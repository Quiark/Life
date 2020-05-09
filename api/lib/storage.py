import os
from os.path import join
from typing import List
from lib.common import lstrip_if
import config

class Storage:
    def get_group_path(self, groupid: str) -> str:
        return join(config.STORAGE_PREFIX, groupid, '')

class LocalStorage(Storage):
    def __init__(self):
        self.path = config.LOCAL_STORAGE
        os.makedirs(self.path, exist_ok=True)

    def put_object(self, Key, Body):
        fullpath = join(self.path, Key)
        directory = os.path.dirname(fullpath)
        os.makedirs(directory, exist_ok=True)
        with open(fullpath, 'w') as it:
            it.write(Body)

    def get_object(self, Key) -> bytes:
        fullpath = join(self.path, Key)
        with open(fullpath) as it:
            return it.read()

    # not specific to group, just a FS path and returns names only
    def list_items(self, path: str, prefix: str) -> List[str]:
        return [it for it in os.listdir(join(self.path, path)) if it.startswith(prefix)]

    def rename(self, fr: str, to: str):
        os.rename(join(self.path, fr),
                  join(self.path, to))

    def get_upload_details(self):
        return {}


class UnpublishedList:
    def __init__(self, list: List[str]):
        self.all_filelist = list
        self.extmap = {}
        for it in list:
            name, ext = os.path.splitext(it)
            self.extmap[name] = ext

    def get_response(self) -> List:
        filelist = filter(lambda x: x.startswith(config.IMG_PREVIEW_PREFIX), self.all_filelist)

        response = []
        for x in filelist:
            name, ext = os.path.splitext(x)
            orig_file = name[len(config.IMG_PREVIEW_PREFIX):]
            orig_ext = self.extmap[orig_file]
            response.append({
                'id': lstrip_if(name, config.IMG_PREVIEW_PREFIX),
                'format': orig_ext.lstrip('.'),
                'filename': x
            })
        return response

