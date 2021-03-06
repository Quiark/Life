import os
import json
import logging
from os.path import join
from datetime import datetime

import config
from lib.database import Database
from lib.storage import Storage
from lib.data import Post



# Deprecated
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


class PostCreatorV2():
    def __init__(self, storage: Storage, db: Database, unpub_id: str, ext: str):
        self.storage = storage
        self.db = db

        # with ext, no prefix
        self.unpub_id = unpub_id
        #self.ext = os.path.splitext(unpub_id)[1].strip('.')
        self.ext = ext

    def publish(self, groupid: str, text: str):
        if text == None: text = '  ' # dynamodb abhors an empty string
        now = datetime.utcnow()
        data = Post(
                groupid,
                None,  # to be filled later
                text,
                [],
                format=self.ext,
                time=now
        )
        # save to DB .. these steps are not exactly atomic
        data = self.db.add_post(data)

        # move the file
        self.storage.rename(
                f"{config.STORAGE_PREFIX}{config.UNPUBLISHED_GROUP}/{self.unpub_id}.{self.ext}",
                f"{config.STORAGE_PREFIX}{groupid}/{data.postid}.{self.ext}"
        )
        try:
            # preview is always a still picture .jpg
            suffix = ''
            self.storage.rename(
                    f"{config.STORAGE_PREFIX}{config.UNPUBLISHED_GROUP}/{config.IMG_PREVIEW_PREFIX}{self.unpub_id}{suffix}{config.IMG_EXT}",
                    f"{config.STORAGE_PREFIX}{groupid}/{config.IMG_PREVIEW_PREFIX}{data.postid}{config.IMG_EXT}"
            )
        except Exception as e:
            logging.exception('cant move preview image')

        if False and self.ext != 'jpg':
            # also move preview video
            try:
                self.storage.rename(
                        f"{config.STORAGE_PREFIX}{config.UNPUBLISHED_GROUP}/{config.IMG_PREVIEW_PREFIX}{self.unpub_id}.{self.ext}",
                        f"{config.STORAGE_PREFIX}{groupid}/{config.IMG_PREVIEW_PREFIX}{data.postid}.{self.ext}"
                )
            except Exception as e:
                logging.exception('cannot move video preview')
