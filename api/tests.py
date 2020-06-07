import os
import sys
sys.path.append('.')

import config
config.DYNAMO_IMPL = 'mock'
config.STORAGE_IMPL = 'local'

import base
from lib.storage import LocalStorage
from lib.database import MockDatabase
from lib.posts import PostCreatorV2

def mk_image(path: str):
    with open(path, 'w') as outf:
        outf.write('abcd')

def test_posting():
    stor = base.storage
    assert(type(stor) is LocalStorage)
    assert(type(base.db) is MockDatabase)
    prefix = os.path.join(stor.path, config.STORAGE_PREFIX, config.UNPUBLISHED_GROUP)
    mk_image(f'{prefix}/timage.jpg')
    mk_image(f'{prefix}/p500-timage.jpg')

    mk_image(f'{prefix}/tvid.mov')
    mk_image(f'{prefix}/p500-tvid.mov')
    mk_image(f'{prefix}/p500-tvid{config.VIDEO_PREVIEW_SUFFIX}.jpg')


    pc = PostCreatorV2(stor, base.db, 'timage', 'jpg')
    pc.publish('zzz', 'timage')
    

    pc = PostCreatorV2(stor, base.db, 'tvid', 'mov')
    pc.publish('zzz', 'tvid')
