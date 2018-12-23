from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import asdict, is_dataclass
import base
from lib.data import Comment, Post, Group, User, LifeApp

app = Flask(__name__)
# TODO whitelist S3 static sites only
CORS(app)
# TODO facebook-less event management

CURRENT_USERID = 'admin'

# --- middleware ---
def to_popo(obj):
    if type(obj) is list:
        return list(to_popo(i) for i in obj)
    elif type(obj) is dict:
        return {k: to_popo(obj[k]) for k in obj}
    elif is_dataclass(obj):
        return asdict(obj)
    else:
        return obj

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
            else:
                raise AuthorizationError('incorrect password')
        request.Life.inited = True

def user_must_ingroup(groupid: str):
    load_user()
    if not (groupid in request.Life.user.groups):
        raise AuthorizationError('group')

# --- routes ---
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/groups/<groupid>')
def get_group(groupid):
    return respond(base.db.get_group(groupid))

@app.route('/groups/<groupid>/page/<page>')
def get_posts_by_page(groupid, page):
    user_must_ingroup(groupid)
    result = base.db.get_posts_by_page(groupid, page)
    return respond(result)


@app.route('/posts', methods=['POST'])
def create_post():
    dat = request.get_json()
    # TODO
    #

@app.route('/groups/<groupid>/posts/<postid>/comments', methods=['POST'])
def create_comment(groupid, postid):
    user_must_ingroup(groupid)
    dat = request.get_json()
    cmnt = Comment(
            author=CURRENT_USERID,
            text=dat['text'])
    base.db.add_comment(groupid, postid, cmnt)
    return 'ok'


@app.route('/user')
def get_user():
    load_user()
    return respond(request.Life.user)
