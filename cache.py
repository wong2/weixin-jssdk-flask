#-*-coding:utf-8-*-

from flask.ext.cache import Cache
from config import CACHE_CONFIG

cache = Cache(config=CACHE_CONFIG)
