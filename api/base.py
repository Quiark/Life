import os
import json
# TODO remove jinja2 from lambda installation
import config
import lib.common
from lib.storage import LocalStorage
import lib.s3
from lib.posts import PostCreator
from lib.database import MockDatabase
from lib.dynamodb import DynamoDatabase
from lib.types import TypescriptDefs

if config.DYNAMO_IMPL == 'local':
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '../.dynamodb_local.txt'
elif config.DYNAMO_IMPL == 'aws':
    if config.API_LOCAL:
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '../.dynamodb_creds.txt'
    else:
        # using env variables
        pass


if config.STORAGE_IMPL == 's3':
    storage = lib.s3.S3Storage()
else:
    storage = lib.storage.LocalStorage()

if config.DYNAMO_IMPL == 'mock':
    db = MockDatabase()
else:
    db = DynamoDatabase()

# export config to javascript
if config.API_LOCAL:
    lib.common.export_defs('../ui/src')

if config.DYNAMO_IMPL == 'local':
    import lib.dynamodb
    admin = lib.dynamodb.DynamoAdmin()
    print(admin.get_users())
