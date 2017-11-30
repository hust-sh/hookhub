# coding: utf-8
'''
A webhook hub.
'''

from flask import Flask, Blueprint, request
from flask_restful import Api, Resource, url_for
from common.utils import SiteLocator
import logging
import json

logging.basicConfig(filename='/var/log/flask.log',level=logging.DEBUG)

app = Flask(__name__)

blueprint = Blueprint('admin',  __name__)


@blueprint.route('/webhook/<string:site>', methods=['GET', 'POST'])
def webhook(site):

    data = request.get_json()
    logging.info('\n[{begin}\n<^>\n{data}\n<^>\n{end}]\n'.format(begin=site, data=formating(data), end=site))

    with SiteLocator.get_factory(site) as client_cls:

        msg = client_cls.transform_data(data)
        resp = client_cls.send_message(msg)
        logging.info("resp: %s", resp)

    return 'ok'

'''
    if site == 'jira':
        msg = Jira.transform_data(data)
        resp = Jira.send_message(msg)
        logging.info("jira does: %s", resp)
    elif site == 'jenkins':
        msg = Jenkins.transform_data(data)
        resp = Jenkins.send_message(msg)
        logging.info("jenkins dose: %s", resp)
'''



app.register_blueprint(blueprint)



@app.route('/test')
def test():

    return url_for('admin.webhook', access_token='abc123',  _external=True)

'''
@app.route('/webhook/gitlab', methods=['GET', 'POST'])
def gitlab():

    data = request.get_json()
    logging.info('\n[gitlab\n<^>\n{data}\n<^>\ngitlab]\n'.format(data=formating(data)))
    return 'ok'

@app.route('/webhook/jira', methods=['GET', 'POST'])
def jira():

    data = request.get_json()
    logging.info('\n[jira\n<^>\n{data}\n<^>\njira]\n'.format(data=formating(data)))
    return 'ok'
'''

def formating(data):

    return json.dumps(data, indent=2)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3002)
