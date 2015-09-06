#-*-coding:utf-8-*-

from fnmatch import fnmatch
from flask import Flask, request, jsonify
from raven.contrib.flask import Sentry
from config import APP_ID, APP_SECRET, SENTRY_DSN, ALLOWED_DOMAINS
from cache import cache
from sign import Signer

app = Flask(__name__)
cache.init_app(app)

if SENTRY_DSN:
    app.config['SENTRY_DSN'] = SENTRY_DSN
    sentry = Sentry(app)


signer = Signer(APP_ID, APP_SECRET)

@app.route('/sign')
def sign():
    url = request.args.get('url')
    assert url and any(fnmatch(url, p) for p in ALLOWED_DOMAINS)
    ret = signer.sign(url)
    resp = jsonify(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
