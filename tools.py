import os
import sys
import subprocess
import argparse




parser = argparse.ArgumentParser(description='Life tooling')
parser.add_argument('operation', type=str, choices=['dynamodb', 'ui_deploy', 'exportconfig', 'uplambda'],
                    help='an integer for the accumulator')

args = parser.parse_args()


def dynamodb():
    import api.config as config
    # this should not depend on the virtualenv

    subprocess.run('java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb',
                    shell=True, cwd=config.DYNAMODB_LOCAL_PATH)

def s3_deploy():
    sys.path.append('api')
    import config
    import lib.s3

    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.dynamodb_creds.txt'
    # if not isinstance(base.storage, lib.s3.S3Storage):
    #     print('not configured for S3 (in config.py)')
    #     sys.exit()

    storage = lib.s3.S3Storage()
    storage.upload_file('ui/index.prod.html', 'index.html')
    storage.upload_file('ui/favicon.png', 'favicon.png')
    #storage.upload_file('ui/dist/bundle.js', 'bundle.js')

    def upload_avatar(name):
        storage.upload_file('runtime/storage/avatars/' + name + '.jpg', 'storage/avatars/' + name + '.jpg')

    #upload_avatar('admin')
    #upload_avatar('katrina')
    #upload_avatar('jitka')
    #upload_avatar('lucyngai')
    #upload_avatar('ondra')

def export_config():
    sys.path.append('api')
    import lib.common

    lib.common.export_defs('ui/src')

def up_lambda():
    subprocess.check_call('npm pack', shell=True, cwd='aws-lambda-image')
    subprocess.check_call('aws lambda update-function-code --profile default --function-name life-imgresizer --zip-file fileb://aws-lambda-image/package.zip', shell=True)


if args.operation == 'dynamodb':
    dynamodb()
elif args.operation == 's3_deploy':
    s3_deploy()
elif args.operation == 'exportconfig':
    export_config()
elif args.operation == 'uplambda':
    up_lambda()
