# coding: utf-8
'''
A webhook hub.
'''

from flask import Flask
from flask_restful import url_for
from views import blueprint
import logging
logging.basicConfig(filename='/var/log/debug.log',level=logging.DEBUG)

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route('/test')
def test():

    from common.cache import get_redis
    cli = get_redis()
    pipe = cli.pipeline()
    pipe.set('yangluo', 'fizz')
    res = pipe.execute()
    return str(res)



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3002)
