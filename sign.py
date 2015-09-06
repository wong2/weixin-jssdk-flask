#-*-coding:utf-8-*-

import time
import hashlib
import random
import string
import requests
from cache import cache

CACHE_EXPIRE_TIME = 7200


class GetAccessTokenError(Exception):
    pass

class GetTicketError(Exception):
    pass


class Signer(object):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def __repr__(self):
        return '%s (%s)' % (self.__class__.__name__, self.app_id)

    def sign(self, url):
        ret = {
            'nonceStr': self._create_nonce_str(),
            'jsapi_ticket': self.get_ticket(),
            'timestamp': self._create_timestamp(),
            'url': url
        }
        s = '&'.join('%s=%s' % (key.lower(), value) for key, value in sorted(ret.items()))
        ret['signature'] = hashlib.sha1(s).hexdigest()
        return ret

    @cache.memoize(CACHE_EXPIRE_TIME)
    def get_ticket(self):
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        token = self.get_access_token()

        r = requests.get(url, params={
            'access_token': token,
            'type': 'jsapi',
        })
        resp = r.json()
        if resp.get('errcode', 0) != 0:
            raise GetTicketError(resp)

        return resp['ticket']

    @cache.memoize(CACHE_EXPIRE_TIME)
    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        r = requests.get(url, params={
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret,
        })
        resp = r.json()
        if resp.get('errcode', 0) != 0:
            raise GetAccessTokenError(resp)


        return resp['access_token']

    def _create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def _create_timestamp(self):
        return int(time.time())
