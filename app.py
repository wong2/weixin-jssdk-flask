#-*-coding:utf-8-*-

from flask import Flask, request, jsonify
from config import APP_ID, APP_SECRET
from cache import cache
from sign import Signer


app = Flask(__name__)
cache.init_app(app)

signer = Signer(APP_ID, APP_SECRET)


@app.route('/api')
def api():
    url = request.args['url']
    ret = signer.sign(url)
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)
