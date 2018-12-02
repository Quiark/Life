from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import asdict, is_dataclass
import base
from lib.data import Comment, Post, Group, User

app = Flask(__name__)
# TODO whitelist S3 static sites only
CORS(app)

CURRENT_USERID = 'admin'

# --- middleware ---
def to_popo(obj):
    print(obj, type(obj))
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

# --- routes ---
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/groups/<groupid>')
def get_group(groupid):
    return respond(base.db.get_group(groupid))

@app.route('/groups/<groupid>/page/<page>')
def get_posts_by_page(groupid, page):
    result = base.db.get_posts_by_page(groupid, page)
    return respond(result)


@app.route('/posts', methods=['POST'])
def create_post():
    dat = request.get_json()
    # TODO
    #

@app.route('/groups/<groupid>/posts/<postid>/comments', methods=['POST'])
def create_comment(groupid, postid):
    dat = request.get_json()
    cmnt = Comment(
            ix=None,
            author=CURRENT_USERID,
            text=dat['text'])
    base.db.add_comment(groupid, postid, cmnt)
    return 'ok'


@app.route('/user')
def get_user():
    return respond(base.db.get_user('admin'))
