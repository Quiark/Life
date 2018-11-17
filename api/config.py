# Cloud Deployment with Now 2
BUCKET_NAME='life.rplasil.name'
BUCKET_URL=BUCKET_NAME + '.s3-website.' + 'ap-northeast-2.amazonaws.com'

FIRST_GROUP='avz84Ok3xhPBtkoNne-family'

TEMPLATES = './'



# LOCAL DEPLOYMENT
if 1:
    TEMPLATES = 'templates/'
    LOCAL_STORAGE = '/Users/roman/Devel/Life/runtime/storage'
