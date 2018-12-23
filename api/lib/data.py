from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

# this is as stored in DynamoDB

@dataclass
class Comment:
    author: str
    text: str
    time: datetime = datetime.utcnow()

# TODO what are the keys and what are the indexes?
@dataclass
class Post:
    # PARTITION KEY: groupid + postid
    # SORT KEY: postid
    groupid: str
    # refers to image on S3 but not gettable by id
    # unique within the group
    postid: str
    # yes?
    text: str
    comments: List[Comment]
    time: datetime = datetime.utcnow()

    def page(self) -> str:
        return self.postid[:6]

    def partitionid(self) -> str:
        return Post_partition_id(self.groupid, self.postid)


def Post_partition_id(groupid, postid) -> str:
    return groupid + postid[:6]


@dataclass
class Group:
    groupid: str

    # pageid -> next id of post
    # pageid is 201804 for april of 2018
    pages: Dict[str, int]

    colour: str = 'blue'

@dataclass
class User:
    id: str
    name: str
    token: str

    groups: List[Group]

@dataclass
class LifeApp:
    user: Optional[User]
    inited: bool  # only for the user attribute actually
