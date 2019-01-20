import os
from os.path import join
from typing import List
import boto3
import config
from lib.storage import Storage

class S3Storage(Storage):
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = config.BUCKET_NAME

    def strip_expected_prefix(self, prefix: str, fr: str) -> str:
        if not fr.startswith(prefix): raise RuntimeError()
        return fr[len(prefix):]

    def list_items(self, path: str, prefix: str) -> List[str]:
        resp = self.s3.list_objects(
                Bucket=self.bucket,
                Prefix=join(path, prefix))
        cont = resp.get('Contents', None)
        if cont == None: return []
        return [self.strip_expected_prefix(path, x['Key']) for x in cont]

    def rename(self, fr: str, to: str):
        self.s3.copy_object({
            'Bucket': self.bucket,
            'Key': fr
            }, self.bucket, to)
        self.s3.delete_object(Bucket=self.bucket, Key=fr)
