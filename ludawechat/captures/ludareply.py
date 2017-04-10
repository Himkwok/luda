import configparser
import logging
import pprint
import random
import re
from wxpy.ext.talk_bot_utils import get_context_user_id, next_topic
from wxpy.utils import enhance_connection
from ludawechat.captures.capturewebpage import DoCapture

import requests

logger = logging.getLogger(__name__)


class Luda(object):
    '''luda 回复'''
    url = ''

    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read('config/wechat.cfg')
    remoteweb = cf.get('WECHAT_CONFIG', 'ROMOTE_WEB')

    def __init__(self, api_key=None):
        self.session = requests.Session()
        enhance_connection(self.session)
        # noinspection SpellCheckingInspection
        self.api_key = api_key or '7c8cdb56b0dc4450a8deef30a496bd4c'
        self.last_member = dict()

    def is_last_member(self, msg):
        if msg.member == self.last_member.get(msg.chat):
            return True
        else:
            self.last_member[msg.chat] = msg.member

    def do_reply(self, msg, at_member=True):
        # print("*******************************" + msg.text)
        """
        回复消息，并返回答复文本

        :param msg: Message 对象
        :param at_member: 若消息来自群聊，回复时 @发消息的群成员
        :return: 答复文本
        """
        ret = self.reply_text(msg, at_member)
        msg.chat.send(ret[0])
        msg.chat.send_image('captures/' + ret[1])
        # return ret

    def reply_text(self, msg, at_member=True):
        """
        仅返回消息的答复文本

        :param msg: Message 对象
        :param at_member: 若消息来自群聊，回复时 @发消息的群成员
        :return: 答复文本
        """

        def process_answer():

            logger.debug('luda answer:\n' + pprint.pformat(answer))

            ret = str()
            if at_member:
                if len(msg.chat) > 2 and msg.member.name and not self.is_last_member(msg):
                    ret += '@{} '.format(msg.member.name)

            code = -1
            r = DoCapture.do_capture(self.remoteweb +'/qstb/3')  # self.session.post(self.url, json=payload)
            # print(ret)
            return [ret, r]

        def get_location(_chat):

            province = getattr(_chat, 'province', None) or ''
            city = getattr(_chat, 'city', None) or ''

            if province in ('北京', '上海', '天津', '重庆'):
                return '{}市{}区'.format(province, city)
            elif province and city:
                return '{}省{}市'.format(province, city)

        if not msg.bot:
            raise ValueError('bot not found: {}'.format(msg))

        if not msg.text:
            return

        from wxpy.api.chats import Group
        if at_member and isinstance(msg.chat, Group) and msg.member:
            location = get_location(msg.member)
        else:
            # 使该选项失效，防止错误 @ 人
            at_member = False
            location = get_location(msg.chat)

        from wxpy.api.messages import Message
        from wxpy.api.chats import Group

        # 当 msg 不为消息对象时，返回 None
        if not isinstance(msg, Message):
            return

        if isinstance(msg.sender, Group):
            user = msg.member
        else:
            user = msg.sender

        max_len = 32
        re_sub = r'[^a-zA-Z\d]'

        user_id = re.sub(re_sub, '', user.user_name)

        user_id = user_id[-max_len:]

        if location:
            location = location[:30]

        from wxpy.api.chats import Group

        text = msg.text

        if isinstance(msg.chat, Group):
            name = msg.chat.self.name
            text = re.sub(r'\s*@' + re.escape(name) + r'\u2005?\s*', '', text)

        info = str(text)[-30:]

        payload = dict(
            key=self.api_key,
            info=info,
            user_id=user_id,
            loc=location
        )

        logger.debug('luda payload:\n' + pprint.pformat(payload))

        # noinspection PyBroadException
        try:
            r = DoCapture.do_capture(self.remoteweb + '/qstb/3')  # self.session.post(self.url, json=payload)
            answer = r
        except:
            answer = None
        finally:
            return process_answer()
