# Cloud Deployment with Now 2
BUCKET_NAME='life.rplasil.name'
BUCKET_URL=BUCKET_NAME + '.s3-website.' + 'ap-northeast-2.amazonaws.com'

FIRST_GROUP='avz84Ok3xhPBtkoNne-family'

TEMPLATES = './'



API_BASE = 'https://AAAA-now.sh/api/'

# LOCAL DEPLOYMENT
LOCAL = True

if LOCAL:
    TEMPLATES = 'templates/'
    LOCAL_STORAGE = '/Users/roman/Devel/Life/runtime/storage'

    # relative to index.html, what URL are groups under
    STORAGE_PREFIX = 'storage/'

    API_BASE = 'http://localhost:7004/'
