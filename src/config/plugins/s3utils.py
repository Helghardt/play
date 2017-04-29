import os

# Get AWS configs
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_QUERYSTRING_AUTH = False

# Get S3 configs
AWS_USE_S3 = os.environ.get('AWS_USE_S3', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

GOOGLE_CLOUD = os.environ.get('GOOGLE_CLOUD', '')
GOOGLE_CLOUD_STORAGE_BUCKET = os.environ.get('GOOGLE_STORAGE_BUCKET_NAME', '')
GOOGLE_CLOUD_STORAGE_URL = 'https://storage.cloud.google.com/%s' % GOOGLE_CLOUD_STORAGE_BUCKET
GOOGLE_CLOUD_STORAGE_DEFAULT_CACHE_CONTROL = "public, max-age: 7200"

# Evaluate using string due to config files return strings
if AWS_USE_S3 == 'True':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    MEDIA_URL = AWS_S3_URL + '/media/'

if GOOGLE_CLOUD == 'True':
    DEFAULT_FILE_STORAGE = "django_google_cloud_storage.GoogleCloudStorage"
    MEDIA_URL = GOOGLE_CLOUD_STORAGE_URL + '/media/'

