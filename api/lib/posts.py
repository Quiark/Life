import os

import config


class PostCreator():
    def __init__(self, jinja, storage, groupid: str, imgpath: str):
        '''imgpath is relative to groupid'''
        self.storage = storage
        self.imgpath = imgpath
        self.jinja = jinja
        self.groupid = groupid
        
        self.post_tpl = self.jinja.get_template('post.html')

    def html(self):
        return self.post_tpl.render(
                imgpath=f"{self.groupid}/{self.imgpath}"
                )

    def post_path(self):
        base = os.path.splitext(self.imgpath)[0]
        return f"{self.groupid}/{base}.html"

    def run(self):
        self.storage.put_object(Key=self.post_path(), Body=self.html())
