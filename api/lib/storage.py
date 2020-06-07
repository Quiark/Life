import os
import logging
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
        logging.debug('Rename [] to []'.format(fr, to))
        os.rename(join(self.path, fr),
                  join(self.path, to))

    def get_upload_details(self):
        return {
                'aws_s3_url': '/',
                'fields': {
                    'storage': 'LocalStorage',
                    'key': 'password'
                }}


class UnpublishedList:
    def __init__(self, list: List[str]):
        self.all_filelist = list
        self.extmap = {}
        for it in list:
            name, ext = os.path.splitext(it)
            self.extmap[name] = ext

    '''
    newly generated video files

    API call in lambda sets the destination to storage/unpublished/p500-

    so files generated are

    p500-99b1f8ce5312b2d4fc07a3c3d45eb5b9.0000000.jpg
    p500-99b1f8ce5312b2d4fc07a3c3d45eb5b9.jpg  // <- empty fake
    p500-99b1f8ce5312b2d4fc07a3c3d45eb5b9.mp4
    '''

    def get_response(self) -> List:
        filelist = filter(lambda x: x.startswith(config.IMG_PREVIEW_PREFIX), self.all_filelist)

        response = []
        for x in filelist:
            name, ext = os.path.splitext(x)
            orig_file = name[len(config.IMG_PREVIEW_PREFIX):]
            if orig_file.endswith(config.VIDEO_PREVIEW_SUFFIX):
                orig_file = orig_file[:-len(config.VIDEO_PREVIEW_SUFFIX)]
            # disable listing video files directly because they all now have a thumbnail
            if (orig_file in self.extmap):
                if ext == '.jpg':
                    orig_ext = self.extmap[orig_file]
                    response.append({
                        'id': lstrip_if(orig_file, config.IMG_PREVIEW_PREFIX),
                        'format': orig_ext.lstrip('.'),
                        'filename': x
                    })
            else:
                logging.info('orig_ext not found for {}'.format(orig_file))
        return response

