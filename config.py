#-*-coding:utf-8-*-

APP_ID = ''
APP_SECRET = ''

# https://pythonhosted.org/Flask-Cache/#configuring-flask-cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://user:password@localhost:6379/0',
}

ALLOWED_HOSTS = ['*']

SENTRY_DSN = ''

try:
    from local_config import *
except ImportError:
    pass
