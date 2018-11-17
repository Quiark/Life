import os
from os.path import join
import config

# imitates boto3 s3 api
class LocalStorage:
    def __init__(self):
        self.path = config.LOCAL_STORAGE
        os.makedirs(self.path, exist_ok=True)

    def put_object(self, Key, Body):
        fullpath = join(self.path, Key)
        directory = os.path.dirname(fullpath)
        os.makedirs(directory, exist_ok=True)
        with open(fullpath, 'w') as it:
            it.write(Body)

