from flask import Flask, jsonify, request
from flask_cors import CORS
import base

app = Flask(__name__)
# TODO whitelist S3 static sites only
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# will be in a static file on S3, I think
@app.route('/posts/<groupid>')
def get_posts(groupid):
    return jsonify(['IMG_5634', 'abc1'])


@app.route('/posts/<postid>', methods=['POST'])
def create_post(postid):
    dat = request.get_json()



@app.route('/posts/<postid>/comments', methods=['POST'])
def create_comment(postid):
    pass
