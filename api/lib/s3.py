import os
import base64
import hmac
import hashlib
import json
from os.path import join
from typing import List
import boto3
import config
from lib.storage import Storage
from lib.common import aws_api_args

class S3Storage(Storage):
    def __init__(self):
        kwargs = aws_api_args()
        self.s3 = boto3.client('s3', **kwargs)
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
        self.s3.copy_object(
                CopySource={
                    'Bucket': self.bucket,
                    'Key': fr
                },
                Bucket=self.bucket,
                Key=to)
        self.s3.delete_object(Bucket=self.bucket, Key=fr)

    def upload_file(self, fr: str, to: str):
        with open(fr, 'rb') as inf:
            ext = os.path.splitext(fr)[-1].lower()
            if ext == '.html': ct = 'text/html'
            elif ext == '.js': ct = 'application/javascript'
            elif ext == '.png': ct = 'image/png'
            elif (ext == '.jpg') or (ext == '.jpeg'): ct = 'image/jpeg'

            return self.s3.put_object(
                        Body=inf,
                        Bucket=self.bucket,
                        Key=to,
                        ContentType=ct)

    def get_upload_details(self):
        policy = self.gen_policy()
        creds = self.s3._request_signer._credentials
        if False:
            '''
            creds = self.s3._request_signer._credentials
            secret = creds.secret_key
            signature, policy = self.sign_policy(policy, secret)
            return {
                'signature': signature,
                'policy': policy,
                'access_key': creds.access_key
            }
            '''
        else: # new version
            '''
            kwargs = {
                    # aws_api_args()
                'aws_access_key_id': creds.access_key,
                'aws_secret_access_key': creds.secret_key
            }
            '''
            kwargs = aws_api_args()
            #boto3.config.add_section('s3')
            #boto3.config.set('s3', 'use-sigv4', 'True')
            s3client = boto3.client('s3',
                    region_name=config.UPLOAD_ENDPOINT,
                    #host='s3.ap-northeast-2.amazonaws.com',
                    **kwargs)
            #s3client = self.s3
            post = s3client.generate_presigned_post(
                    Bucket=config.UPLOAD_BUCKET,
                    Key='${filename}',
                    Conditions=self.gen_policy()
                    )
            return post

    def gen_policy(self):
        bucket_name = config.UPLOAD_BUCKET
        max_byte_size = 16 * 1024 * 1024
        return [
                { "bucket" : bucket_name },
                #[ "starts-with", "$key", ""],
                { "acl" : "private"},
                [ "content-length-range", 0, max_byte_size ]
                #{"x-amz-algorithm": "AWS4-HMAC-SHA256"}
                #{"x-amz-date": "20151229T000000Z" }

        ]
