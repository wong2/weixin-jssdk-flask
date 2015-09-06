#-*-coding:utf-8-*-

from fnmatch import fnmatch
from flask import Flask, request, jsonify, abort
from raven.contrib.flask import Sentry
from config import APP_ID, APP_SECRET, SENTRY_DSN, ALLOWED_HOSTS
from cache import cache
from sign import Signer
from utils import extract_hostname

app = Flask(__name__)
cache.init_app(app)

if SENTRY_DSN:
    app.config['SENTRY_DSN'] = SENTRY_DSN
    sentry = Sentry(app)


signer = Signer(APP_ID, APP_SECRET)


def _is_allowed_url(url):
    host = extract_hostname(url)
    return host and any(fnmatch(host, p) for p in ALLOWED_HOSTS)

@app.route('/sign')
def sign():
    url = request.args.get('url')
    if not _is_allowed_url(url):
        abort(403)

    ret = signer.sign(url)

    resp = jsonify(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
