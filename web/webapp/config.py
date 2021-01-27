import os
from glob import glob


class Config(object):
    # Overwrite env vars with a secret if available
    for var in glob('/run/secrets/*'):
        k = var.split('/')[-1].upper()
        v = open(var).read().rstrip('\n')
        os.environ[k] = v
        # print(f'export {k}={v}')

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', '/static')
    DEBUG = os.getenv('DEBUG', False)
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    FLASKS3_ENDPOINT_URL = os.getenv('FLASKS3_ENDPOINT_URL')
    FLASKS3_BUCKET_DOMAIN = os.getenv('FLASKS3_BUCKET_DOMAIN')
    FLASKS3_URL_STYLE = os.getenv('FLASKS3_URL_STYLE', 'path')
    FLASKS3_FORCE_MIMETYPE = os.getenv('FLASKS3_FORCE_MIMETYPE', True)
    FLASKS3_GZIP = os.getenv('FLASKS3_GZIP', True)
    FLASKS3_ONLY_MODIFIED = os.getenv('FLASKS3_ONLY_MODIFIED', True)
    FLASKS3_BUCKET_NAME = os.getenv('FLASKS3_BUCKET_NAME', 'statics')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    JWT_SECRET_KEY = 'SG9wZWxpamsgZ2VicnVpa3QgZWVuIHN0dWRlbnQgZGl0IG9vaXQgbnV0dGlnLg=='
    JWT_IDENTITY_CLAIM = 'sub'
