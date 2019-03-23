import os

# Cloud Deployment with Now 2
BUCKET_NAME='life.rplasil.name'
#BUCKET_URL=BUCKET_NAME + '.s3-website.' + 'ap-northeast-2.amazonaws.com'
BUCKET_URL='https://s3.ap-northeast-2.amazonaws.com/' + BUCKET_NAME + '/'

# todo
UPLOAD_BUCKET='life-upload'
UNPUBLISHED_GROUP='keCxhEChibx-unpublished'

IMG_PREVIEW_PREFIX='p300-'
IMG_PREVIEW_SIZE=300
IMG_EXT='.jpg'

FIRST_GROUP='avz84Ok3xhPBtkoNne-family'
SECOND_GROUP = 'bugcp-kungfu'

DYNAMODB_REGION = 'ap-northeast-2'

# relative to index.html, what URL are groups under
# must end with /
STORAGE_PREFIX = 'storage/'

# set after now deployment, only used in JS frontend
API_BASE = 'https://life.quiark.now.sh'

# LOCAL DEPLOYMENT (this flag is only used in this config)
LOCAL = False

# is api running from local machine or now.sh
API_LOCAL = (os.environ.get('API_LOCAL', 'true')) == 'true'

if LOCAL:
    STORAGE_IMPL = 'local'
    DYNAMO_IMPL = 'local'

    LOCAL_STORAGE = '/Users/roman/Devel/Life/runtime/'

    DYNAMODB_LOCAL_PATH = '/Users/roman/Downloads'

    API_BASE = 'http://localhost:7004/api'

else:
    STORAGE_IMPL = 's3'
    DYNAMO_IMPL = 'aws'
