# Cloud Deployment with Now 2
BUCKET_NAME='life.rplasil.name'
BUCKET_URL=BUCKET_NAME + '.s3-website.' + 'ap-northeast-2.amazonaws.com'

# todo
UPLOAD_BUCKET='life-upload'
UNPUBLISHED_GROUP='keCxhEChibx-unpublished'

IMG_PREVIEW_PREFIX='p300-'
IMG_PREVIEW_SIZE=300
IMG_EXT='.jpg'

FIRST_GROUP='avz84Ok3xhPBtkoNne-family'

TEMPLATES = './'


# relative to index.html, what URL are groups under
# must end with /
STORAGE_PREFIX = 'storage/'

API_BASE = 'https://AAAA-now.sh/api/'

# LOCAL DEPLOYMENT (this flag is only used in this config)
LOCAL = True
STORAGE_IMPL = 's3'

if LOCAL:
    TEMPLATES = 'templates/'
    LOCAL_STORAGE = '/Users/roman/Devel/Life/runtime/'


    API_BASE = 'http://localhost:7004/'
