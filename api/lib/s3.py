import os
from typing import List
import boto3
import config

class S3Storage(Storage):
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = config.BUCKET_NAME

    def strip_expected_prefix(self, prefix: str, fr: str) -> str:
        if not fr.startswith(prefix): raise RuntimeError()
        return fr[len(prefix):]

    def list_items(self, path: str) -> List[str]:
        resp = self.s3.list_objects(
                Bucket=self.bucket,
                Prefix=path)
        return [self.strip_expected_prefix(path, x['Key']) for x in resp['Contents']]
