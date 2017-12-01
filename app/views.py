# coding: utf-8


from flask import Blueprint, request, jsonify
from common.utils import SiteLocator, gen_webhook, gen_access_token, get_webhook
import common.config as const
from common.cache import get_redis
from flask_restful import url_for
import json
from common.log import logger

blueprint = Blueprint('admin',  __name__)


@blueprint.route('/webhook/<string:site>', methods=['POST'])
def webhook(site):

    access_token = request.args.get('access_token')
    data = request.get_json()
    logger().info('\n[{begin}\naccess_token:{token}\n{data}\n{end}]\n'.format(begin=site, token=access_token, data=formating(data), end=site))

    webhook = get_webhook(site, access_token)
    if not webhook:
        return jsonify(ok=False, error='Invalid webhook')

    with SiteLocator.get_factory(site) as client_cls:

        msg = client_cls.transform_data(data)
        resp = client_cls.send_message(webhook, msg)
        logger().info("resp: %s", resp)

    return jsonify(ok=True)


@blueprint.route('/gen_hook/<string:site>', methods=['POST'])
def gen_hook(site):

    if site not in const.WEBHOOK_TYPES:
        return jsonify(ok=False, error='Invalid site. Choose {} Insted.'.format(const.WEBHOOK_TYPES))

    url = request.get_json().get('url')
    if not url:
        return jsonify(ok=True, error='url needed.')

    access_token = gen_access_token()

    redis_cli = get_redis()
    redis_cli.hset(site, access_token, url)
    return jsonify(ok=True, webhook=gen_webhook(site, access_token))



def formating(data):

    return json.dumps(data, indent=2)
