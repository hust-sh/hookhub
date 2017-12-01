# coding: utf-8
"""
"""

import logging
import traceback
import requests
import json


webhook = 'https://oapi.dingtalk.com/robot/send?access_token=4431ce3a5a8ac6d057b34615f254fd5e8df8d5eaa9e9c9303f6751eebd84fb31'


class Jira:
    @classmethod
    def transform_data(cls, data):

        try:
            data = _pre_process_data(data)
            title, text = _assemble_message(data)
            return _pack_response(title=title, text=text)
        except AttributeError as e:
            logging.info('Invalid data format: data={data}\n exception={exc}\n trace={trace}'.\
            format(data=data, exc=e, trace=traceback.format_exc()))
            return {}
        except Exception as e:
            logging.info('Incredible Exception: data={data}\n exception={exc}\n trace={trace}'.\
            format(data=data, exc=e, trace=traceback.format_exc()))
            return {}

    @classmethod
    def send_message(cls, webhook, msg):

        logging.info("msg: %s", msg)
        header = {'Content-type': 'application/json'}
        resp = requests.post(url=webhook, data=json.dumps(msg), headers=header)
        logging.info("resp: %s", resp.json())
        return resp


def _pack_response(title, text):

    text = '#### {} \n{}'.format(title, text)
    return {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
             "text": text
        },
    }


def _pre_process_data(data):

    # 特殊处理issue第一次被comment
    webhook_event = data.get('webhookEvent')
    if webhook_event == 'jira:issue_updated' and ('changelog' not in data) and 'comment' in data:
        data['webhookEvent'] = 'comment_created'
        return data
    return data


def _assemble_message(data):
    webhook_event = data.get('webhookEvent')

    if webhook_event == 'jira:issue_updated':
        change_field = get_change_field(data)
        if change_field == 'status':
            # 操作者改变issue「状态」
            issue_type = get_issue_type(data)
            user_name = get_user_name(data)
            old_status = get_change_from_string(data)
            new_status = get_change_to_string(data)
            summary = get_summary(data)
            issue_url = get_issue_url(data)
            title = '{}更新了{}【{}】的状态'.format(user_name, issue_type, summary)
            text = '由【{}】变为了【{}】\n[点击查看详情]({})'.format(old_status, new_status, issue_url)
            return title, text
        elif change_field == 'Attachment':
            # 操作者在issue中添加了「附件」
            issue_type = get_issue_type(data)
            user_name = get_user_name(data)
            file_name = get_change_to_string(data)
            summary = get_summary(data)
            issue_url = get_issue_url(data)
            title = '{}在{}【{}】中上传了一个新附件【{}】'.format(user_name, issue_type, summary, file_name)
            text = '[点击查看详情]({})'.format(issue_url)
            return title, text
        elif change_field == 'assignee':
            # 操作者在issue中分配/修改了「经办人」
            issue_type = get_issue_type(data)
            user_name = get_user_name(data)
            old_user = get_change_from_string(data)
            new_user = get_change_to_string(data)
            summary = get_summary(data)
            issue_url = get_issue_url(data)
            title = '{}更新了{}【{}】经办人:由【{}】变为了【{}】'.format(user_name, issue_type, summary, old_user, new_user)
            text = '[点击查看详情]({})'.format(issue_url)
            return title, text

        elif change_field == 'duedate':
            # 操作者在issue中修改了「到期时间」
            issue_type = get_issue_type(data)
            user_name = get_user_name(data)
            old_user = get_change_from_string(data)
            new_user = get_change_to_string(data)
            summary = get_summary(data)
            issue_url = get_issue_url(data)
            title = '{}更新了{}【{}】的到期时间，由【{}】转变为【{}】'.format(user_name, issue_type, summary, old_user, new_user)
            text = '[点击查看详情]({})'.format(issue_url)
            return title, text

        elif change_field == '预计启动时间':
            # 操作者在issue中修改了「预计启动时间」
            issue_type = get_issue_type(data)
            user_name = get_user_name(data)
            old_user = get_change_from_string(data)
            new_user = get_change_to_string(data)
            summary = get_summary(data)
            issue_url = get_issue_url(data)
            title = '{}更新了{}【{}】的预计启动时间，由【{}】转变为【{}】'.format(user_name, issue_type, summary, old_user, new_user)
            text = '[点击查看详情]({})'.format(issue_url)
            return title, text

    elif webhook_event == 'jira:issue_created':
        issue_type = get_issue_type(data)
        issue_key = data.get('issue').get('key')
        creator = get_user_name(data)
        summary = get_summary(data)
        assignee = data.get('issue').get('fields').get('assignee').get('displayName')
        issue_url = get_issue_url(data)
        priority = data.get('issue').get('fields').get('priority').get('name')
        description = data.get('issue').get('fields').get('description')

        title = '新增{issue_type}'.format(issue_type=issue_type)
        text = '编号: {issue_key} \n主题: {summary} \n报告人: {creator} \n经办人: {assignee}\n优先级: {priority} \n描述: {description} \n[查看详情]({url}).'
        text = text.format(issue_key=issue_key, summary=summary, creator=creator, assignee=assignee, priority=priority, description=description, url=issue_url)
        return title, text

    elif webhook_event == 'comment_created':
        # 操作者在issue中添加了「评论」
        user_name = data.get('comment').get('author').get('displayName')
        issue_type = get_issue_type(data)
        summary = data.get('issue').get('fields').get('summary')
        issue_url = get_issue_url(data)

        title = '{} 在{} 【{}】中添加了一条新评论'.format(user_name, issue_type, summary)
        text = '[点击查看详情]({})'.format(issue_url)
        return title, text

    elif webhook_event == 'jira:issue_deleted':
        # 操作者删除了一条issue
        user_name = data.get('user').get('displayName')
        issue_type = get_issue_type(data)
        summary = get_summary(data)

        title = '删除{}'.format(issue_type)
        text = '{} 删除了{} 【{}】。'.format(user_name, issue_type, summary)
        return title, text

    return '', ''


def get_issue_url(data):

    issue_key = data.get('issue').get('key')
    return get_issue_url_with_key(issue_key)


def get_issue_url_with_key(issue_key):

    return 'https://jira.bytedance.com/browse/{}'.format(issue_key)


def get_change_field(data):

    return data.get('changelog').get('items')[0].get('field')


def get_user_name(data):

    return data.get('user').get('displayName')


def get_change_from_string(data):

    return data.get('changelog').get('items')[0].get('fromString')


def get_change_from(data):

    return data.get('changelog').get('items')[0].get('from')


def get_change_to(data):

    return data.get('changelog').get('items')[0].get('to')


def get_change_to_string(data):

    return data.get('changelog').get('items')[0].get('toString')


def get_summary(data):

    return data.get('issue').get('fields').get('summary')


def get_issue_type(data):

    return data.get('issue').get('fields').get('issuetype').get('name')


def get_assignee(data):

    return data.get('issue').get('fields').get('assignee').get('name')


def get_creator(data):

    return data.get('issue').get('fields').get('creator').get('name')
