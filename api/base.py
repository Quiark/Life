import os
import json
# TODO remove jinja2 from lambda installation
# from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
import config
from lib.storage import LocalStorage
from lib.posts import PostCreator
from lib.database import MockDatabase
from lib.dynamodb import DynamoDatabase
from lib.types import TypescriptDefs

os.environ['AWS_CONFIG_FILE'] = '../.dynamodb_creds.txt'

jinja = Environment(
    loader=FileSystemLoader(config.TEMPLATES),
    autoescape=select_autoescape(['html', 'xml'])
)

storage = LocalStorage()
db = DynamoDatabase()

#pc = PostCreator(jinja, storage, db, db.p1)


# export config to javascript
with open('../ui/src/config.js', 'w') as it:
    c = config.__dict__
    it.write('module.exports =' + json.dumps({ k: c[k] for k in c if k.upper() == k}))

TypescriptDefs().write_types('../ui/src/data.ts')
