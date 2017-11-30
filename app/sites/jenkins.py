# coding: utf-8

import json
import logging
import traceback
import requests


webhook = 'https://oapi.dingtalk.com/robot/send?access_token=49679eab1c1d2c16af000de2f61e2803a9071cb38b92e16b05c8ba18f007ccaa' 


class Jenkins:

    @classmethod
    def transform_data(cls, data):

        try:
            repo = data.get('display_name')
            url = data.get('build').get('full_url')
            phase = data.get('build').get('phase')
            status = data.get('build').get('status', '')
            title, text = _pack_msg(repo, url, phase, status)
            return _pack_response(title, text)
        except Exception as e:
            logging.info('Incredible Exception: data={data}\n exception={exc}\n trace={trace}'.format(data=data, exc=e, trace=traceback.format_exc()))
            return {}

    @classmethod
    def send_message(cls, msg):

        logging.info('msg: %s', msg)
        header = {'Content-type': 'application/json'}
        resp = requests.post(url=webhook, data=json.dumps(msg), headers=header)
        logging.info("resp: %s", resp.json())
        return resp


def _pack_msg(repo, url, phase, status):

    if phase == 'STARTED':
        title = '开始构建 {}'.format(repo)
    elif phase == 'FINALIZED':
        if status == 'SUCCESS':
            title = '构建成功 {}'.format(repo)
        else:
            title = '构建失败 {}'.format(repo)
    else:
        title = ''
    text = '[点击查看详情]({url})'.format(url=url)
    return title, text


def _pack_response(title, text):

    text = '#### {} \n{}'.format(title, text)
    return {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
             "text": text
        },
    }
