from typing import List, Dict, ClassVar, Optional
from datetime import datetime
import boto3
import dataclasses
import logging
import hashlib
from dataclasses import asdict, is_dataclass, fields

import config
import lib
from lib.data import *
from lib.database import Database
from lib.common import first, aws_api_args
from lib.types import eq_origin

def entity_to_dict(obj):
    t = type(obj)
    res = asdict(obj)
    if t is Post:
        res['partitionid'] = obj.partitionid()
    return res

def entity_from_typed(obj: Dict, cls: type):
    map = _from_typed(obj, cls)
    if cls is Post:
        del map['partitionid']
    elif cls is Comment:
        if 'ix' in map: del map['ix']
    return cls(**map)

def _from_item_typed(v: Dict, typ: Optional[type]):
    def assert_type(expected: Optional[type]):
        if typ == None: return None
        if expected == list:
            if (typ != list) and (not eq_origin(List, typ)):
                raise RuntimeError('Invalid list type')
        elif expected == dict:
            if (typ != dict) and (not is_dataclass(typ)) and (not eq_origin(Dict, typ)):
                raise RuntimeError('Invalid dict type')
        else:
            assert(typ == expected), f"typ: {typ} expected: {expected}"

        if not is_dataclass(typ):
            return typ.__args__[0]
        else:
            return None

    assert type(v) is dict
    val = first(v.values())
    tag = first(v.keys())

    # ClassVar.__args__ contains the type parameters
    if tag == 'M':
        assert_type(dict)
        if is_dataclass(typ):
            val = entity_from_typed(val, typ)
        else:
            val = _from_typed(val)
    elif tag == 'N':
        if typ is datetime:
            val = datetime.fromtimestamp(float(val))
        elif '.' in val:
            val = float(val)
        else:
            val = int(val)
    elif tag == 'L':
        t_inside = assert_type(list)
        val = [_from_item_typed(it, t_inside) for it in val]

    return val

def _get_fields(cls: Optional[type]) -> Dict[str, dataclasses.Field]:
    fs = {}
    if cls == None: return {}
    for it in fields(cls):
        fs[it.name] = it
    return fs

def _from_typed(obj: Dict, cls: type = None) -> Dict:
    fs = _get_fields(cls)
    res = {}
    for k in obj:
        v = obj[k]
        typ = None
        try: typ = fs[k].type
        except AttributeError: pass
        except KeyError: pass

        res[k] = _from_item_typed(v, typ)

    return res

def _to_typed(obj, path: str = ''):
    t = type(obj)
    if t is str:
        return {'S': obj}
    elif (t is int) or (t is float):
        return {'N': str(obj)}
    elif t is bool:
        return {'BOOL': obj}
    elif t is list:
        return {'L': [_to_typed(it[1], f"{path}[{it[0]}]") for it in enumerate(obj)]}
    elif t is dict:
        return {'M': {k: _to_typed(obj[k], f"{path}.{k}") for k in obj}}
    elif is_dataclass(obj):
        return _to_typed(entity_to_dict(obj))
    elif t is datetime:
        return {'N': str(obj.timestamp())}
    else: 
        raise RuntimeError(f"Unknown type {t} in _to_typed at {path}")


def to_dynamo_typed(obj):
    if not is_dataclass(obj):
        raise RuntimeError("This is for dataclasses")

    d = entity_to_dict(obj)
    return _to_typed(d)['M']


TABLE_USERS = 'life-users'
TABLE_GROUPS = 'life-groups'
TABLE_POSTS = 'life-posts'

class DynamoDatabase(Database):
    def __init__(self):
        kwargs = aws_api_args()
        if config.DYNAMO_IMPL == 'local': kwargs['endpoint_url'] = 'http://localhost:8000'
        kwargs['region_name'] = config.DYNAMODB_REGION

        logging.debug('connecting using key id ' + kwargs.get('aws_access_key_id', ''))
        hash = hashlib.sha256(kwargs.get('aws_secret_access_key', '').encode()).hexdigest()
        logging.debug('connecting using sha256(secret): ' + hash)

        self.dynamo = boto3.client('dynamodb', **kwargs)

    def create_tables(self):
        defaults = {
            'AttributeDefinitions': {},
            'ProvisionedThroughput': {
                'WriteCapacityUnits': 5, 
                "ReadCapacityUnits": 5
            },
            'KeySchema': {},

        }

        # TODO create users table
        users = dict(defaults)
        users['TableName'] = TABLE_USERS
        users['AttributeDefinitions'] = [{
            'AttributeName': 'id',
            'AttributeType': 'S'
        }]
        users['KeySchema'] = [{
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }]
        self.dynamo.create_table(**users)

        posts = dict(defaults)
        posts['TableName'] = TABLE_POSTS
        posts['AttributeDefinitions'] = [{
            'AttributeName': 'partitionid',
            'AttributeType': 'S'
        }, {
            'AttributeName': 'postid',
            'AttributeType': 'S'
        }]
        posts['KeySchema'] = [{
            'AttributeName': 'partitionid',
            'KeyType': 'HASH'
        }, {
            'AttributeName': 'postid',
            'KeyType': 'RANGE'
        }]
        self.dynamo.create_table(**posts)

        groups = dict(defaults)
        groups['TableName'] = TABLE_GROUPS
        groups['AttributeDefinitions'] = [{
            'AttributeName': 'groupid',
            'AttributeType': 'S'
        }]
        groups['KeySchema'] = [{
            'AttributeName': 'groupid',
            'KeyType': 'HASH'
        }]
        self.dynamo.create_table(**groups)


        
    def _inc_postix(self, groupid: str, page: str) -> int:
        response = self.dynamo.update_item(TableName=TABLE_GROUPS,
                Key={'groupid': _to_typed(groupid)},
                ReturnValues='UPDATED_NEW',
                UpdateExpression='SET pages.#p = if_not_exists(pages.#p, :default) + :inc',
                ExpressionAttributeValues={
                    ':inc': _to_typed(1),
                    ':default': _to_typed(0)
                },
                ExpressionAttributeNames={
                    '#p': page
        })
        return first(_from_typed(response['Attributes'])['pages'].values())

    def _store_post(self, data: Post):
        db_data = to_dynamo_typed(data)
        self.dynamo.put_item(
                TableName=TABLE_POSTS,
                Item=db_data)

    def add_group(self, data: Group):
        db_data = to_dynamo_typed(data)
        self.dynamo.put_item(
                TableName=TABLE_GROUPS,
                Item=db_data)

    def get_post(self, groupid: str, postid: str) -> Optional[Post]:
        response = self.dynamo.get_item(
                TableName=TABLE_POSTS,
                Key={
                    'partitionid': _to_typed(lib.data.Post_partition_id(groupid, postid)),
                    'postid': _to_typed(postid)
                },
                ConsistentRead=False)
        if 'Item' not in response: return None
        return entity_from_typed(response['Item'], Post)

    def get_group(self, groupid: str) -> Optional[Group]:
        response = self.dynamo.get_item(
                TableName=TABLE_GROUPS,
                Key={
                    'groupid': _to_typed(groupid)
                },
                ConsistentRead=False)
        if 'Item' not in response: return None
        return entity_from_typed(response['Item'], Group)

    def get_groups(self) -> Optional[List[Group]]:
        response = self.dynamo.scan(TableName=TABLE_GROUPS)
        if 'Items' not in response: return None
        return [entity_from_typed(x, Group) for x in response['Items']]

    def get_posts_by_page(self, groupid: str, page: str) -> Optional[List[Post]]:
        response = self.dynamo.query(
                TableName=TABLE_POSTS,
                ConsistentRead=False,
                KeyConditionExpression='partitionid = :p',
                ExpressionAttributeValues={
                    ':p': _to_typed(Post_partition_id(groupid, page + '0000'))
                })
        if 'Items' not in response: return None
        if 'LastEvaluatedKey' in response: raise RuntimeError('Query returned more than one page')
        return [entity_from_typed(it, Post) for it in response['Items']]

    def get_user(self, userid: str) -> Optional[User]:
        response = self.dynamo.get_item(
                TableName=TABLE_USERS,
                Key={
                    'id': _to_typed(userid)
                },
                ConsistentRead=False)
        if 'Item' not in response: return None
        return entity_from_typed(response['Item'], User)

    def add_user(self, data: User):
        db_data = to_dynamo_typed(data)
        self.dynamo.put_item(
                TableName=TABLE_USERS,
                Item=db_data)

    def add_comment(self, groupid: str, postid: str, comment: Comment):
        response = self.dynamo.update_item(
                TableName=TABLE_POSTS,
                Key={
                    'partitionid': _to_typed(Post_partition_id(groupid, postid)),
                    'postid': _to_typed(postid)
                },
                ReturnValues='UPDATED_NEW',
                UpdateExpression='SET comments = list_append(comments, :it)',
                ExpressionAttributeValues={
                    ':it': _to_typed([comment])
                }
        )


class DynamoAdmin(DynamoDatabase):
    def clear_table(self, name, key):
        users = self.dynamo.scan(TableName=name)['Items']
        for it in users:
            self.dynamo.delete_item(TableName=name, Key={key: it[key]})

    def clear_groups(self):
        self.clear_table(TABLE_GROUPS, 'groupid')

    def clear_posts(self, groupid):
        name = TABLE_POSTS
        items = self.dynamo.scan(TableName=name)['Items']
        for it in items:
            self.dynamo.delete_item(TableName=name, Key={key: it[key]})


    def fill_sample_data(self, with_posts=True):
        import lib.database
        mockdb = lib.database.MockDatabase()
        if not with_posts:
            mockdb.g1.pages = {}
            mockdb.g2.pages = {}
        self.add_group(mockdb.g1)
        self.add_group(mockdb.g2)
        self.add_group(mockdb.g3)
        self.add_user(mockdb.users['admin'])

        if with_posts:
            mockdb.mock_post(mockdb.g2, '201701')
            mockdb.mock_post(mockdb.g2, '201702')
            mockdb.mock_post(mockdb.g2, '201704')
            mockdb.mock_post(mockdb.g2, '201704')
            mockdb.mock_post(mockdb.g1, '201601')

            for i in mockdb.posts.values():
                self._store_post(i)

            #self.add_post(mockdb.p1)
            #self.add_post(mockdb.p2)
            #self.add_comment(mockdb.g1.groupid, mockdb.p1.postid, Comment(author='admin', text='autocommnt'))

