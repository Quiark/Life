import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import asdict, is_dataclass, dataclass
from datetime import datetime
from typing import Dict
import base
import config
from lib.data import Comment, Post, Group, User, LifeApp, PostPayload
from lib.common import lstrip_if, display_timestamp
from lib.posts import PostCreatorV2

log = logging.getLogger(None)
# log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(getattr(logging, config.LOGLEVEL))
logging.info('... Starting Life app server ...')

app = Flask(__name__)
CORS(app, origins=config.BUCKET_URL)

# --- middleware ---
def to_popo(obj):
    if type(obj) is list:
        return list(to_popo(i) for i in obj)
    elif type(obj) is dict:
        return {k: to_popo(obj[k]) for k in obj}
    elif is_dataclass(obj):
        return to_popo(asdict(obj))
    elif type(obj) is datetime:
        return display_timestamp(obj)
    else:
        return obj

def from_popo(obj: Dict, cls: type):
    # basic impl at first, should check input for correct types
    return cls(**obj)

def typed_payload(cls: type):
    return from_popo(request.get_json(), cls)

def respond(obj):
    return jsonify(to_popo(obj))

# auth
class AuthorizationError(Exception):
    def __init__(self, kind):
        Exception.__init__(self, kind)


def prep_app_container():
    if not hasattr(request, 'Life'):
        request.Life = LifeApp(None, False)


def load_user():
    prep_app_container()
    if request.Life.inited == False:
        auth = request.headers.get('authorization')
        if auth != None:
            (id, token) = auth.split(' ')
            found = base.db.get_user(id)
            if (found != None) and (found.token == token):
                request.Life.user = found
                logging.info('request from {} for {}'.format(found.name, request.path))
            else:
                raise AuthorizationError('incorrect password')
        request.Life.inited = True

def user_must_ingroup(groupid: str):
    load_user()
    if request.Life.user == None:
        raise AuthorizationError('have to log in')
    if not (groupid in request.Life.user.groups):
        raise AuthorizationError('group')

# --- routes ---
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/hello')
def api_hello_world():
    return 'Hello, World api!'

@app.route('/api/groups/<groupid>')
def get_group(groupid):
    return respond(base.db.get_group(groupid))

@app.route('/api/groups')
def get_groups():
    load_user()
    groupids = request.Life.user.groups
    all = base.db.get_groups()

    return respond([x for x in all if (x.groupid in groupids)])


@app.route('/api/groups/<groupid>/page/<page>')
def get_posts_by_page(groupid, page):
    user_must_ingroup(groupid)
    result = base.db.get_posts_by_page(groupid, page)
    result.sort(key=lambda x: x.postid, reverse=True)
    return respond(result)


@app.route('/api/groups/<groupid>/posts/<postid>/comments', methods=['POST'])
def create_comment(groupid, postid):
    user_must_ingroup(groupid)
    dat = request.get_json()
    cmnt = Comment(
            author=request.Life.user.id,
            text=dat['text'])
    base.db.add_comment(groupid, postid, cmnt)
    return 'ok'


@app.route('/api/user')
def get_user():
    load_user()
    return respond(request.Life.user)

@app.route('/api/groups/unpublished/images')
def get_unpublished_images():
    groupid = config.UNPUBLISHED_GROUP
    user_must_ingroup(groupid)

    # TODO move to dedicated code file
    filelist = base.storage.list_items(
        base.storage.get_group_path(groupid), 
        config.IMG_PREVIEW_PREFIX)

    response = [{
        'id': lstrip_if(os.path.splitext(x)[0], config.IMG_PREVIEW_PREFIX),
        'filename': x
        } for x in filelist]

    return respond(response)

@app.route('/api/groups/unpublished/publish/<imageid>', methods=['POST'])
def publish(imageid: str):
    user_must_ingroup(config.UNPUBLISHED_GROUP)
    dat = typed_payload(PostPayload)
    user_must_ingroup(dat.groupid)

    pc = PostCreatorV2(base.storage, base.db, imageid)
    pc.publish(dat.groupid, dat.text)
    return respond({})

@app.route('/api/upload-details')
def get_upload_details():
    user_must_ingroup(config.UNPUBLISHED_GROUP)
    return respond(base.storage.get_upload_details())
