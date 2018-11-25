import os
import json
import logging

import config
from lib.database import Database
from lib.data import Post


class PostCreator():
    def __init__(self, jinja, storage, db: Database, data: Post):
        '''imgpath is relative to groupid'''
        self.storage = storage
        self.data = data
        self.jinja = jinja
        self.db = db
        
        if ('..' in self.data.groupid) or ('%' in self.data.groupid):
            raise RuntimeError('disallowed characters')
        self.post_tpl = self.jinja.get_template('post.html')

    def html(self):
        return self.post_tpl.render(
                imgpath=f"{self.data.groupid}/{self.data.postid}.jpg"
                )

    def post_path(self):
        return f"{self.data.groupid}/{self.data.postid}.html"

    def index_path(self):
        return f"{self.data.groupid}/{self.data.page()}.json"

    def get_fsdata(self):
        try:
            return json.loads(self.storage.get_object(Key=self.index_path()))
        except:
            # TODO detect properly if missing or connection fail
            logging.warning(f"file {self.index_path} not found")
            return []

    def put_fsdata(self, obj):
        return self.storage.put_object(Key=self.index_path(),
                Body=json.dumps(obj))

    def run(self):
        # S3 file storage
        self.storage.put_object(Key=self.post_path(), Body=self.html())

        self.db.save_post(self.data)

        index = self.get_fsdata()
        index.append(self.data.postid)
        self.put_fsdata(index)

