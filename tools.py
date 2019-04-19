import os
import sys
import subprocess
import argparse




parser = argparse.ArgumentParser(description='Life tooling')
parser.add_argument('operation', type=str, choices=['dynamodb', 'ui_deploy'],
                    help='an integer for the accumulator')

args = parser.parse_args()


def dynamodb():
    import api.config as config
    # this should not depend on the virtualenv

    subprocess.run('java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb',
                    shell=True, cwd=config.DYNAMODB_LOCAL_PATH)

def ui_deploy():
    sys.path.append('api')
    import config
    import lib.s3

    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.dynamodb_creds.txt'
    # if not isinstance(base.storage, lib.s3.S3Storage):
    #     print('not configured for S3 (in config.py)')
    #     sys.exit()

    storage = lib.s3.S3Storage()
    storage.upload_file('ui/index.prod.html', 'index.html')
    storage.upload_file('ui/dist/bundle.js', 'bundle.js')

if args.operation == 'dynamodb':
    dynamodb()
elif args.operation == 'ui_deploy':
    ui_deploy()
