# coding:utf-8
import requests
from wxpy import *
import os
import configparser
import jieba
import codecs
from threading import Thread

from ludawechat import *
from ludawechat.captures.ludareply import *

# 读取配置文件
# cf = configparser.ConfigParser()
# cf.read_file(codecs.open(filename="config/wechat.cfg", encoding='utf-8'))
# listen_group = cf.get("WECHAT_CONFIG", "LISTEN_GROUP")
# print(listen_group)

# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)
group = bot.groups().search('代号：鲁达')[0]

# 打印所有群成员
for member in group:
    print(member)

# 获取所有已经配置的应用
r = requests.get('http://127.0.0.1:9001/api/applications')
print(r.json())
for app in r.json():
    jieba.suggest_freq((app['appName']), True)
    # print(x['appName'])

ludareply = Luda(api_key='7c8cdb56b0dc4450a8deef30a496bd4c')


# @bot.register(me)
# def reply_my_friend(msg):
#     seg_list = jieba.cut(msg.text, cut_all=False)
#     for x in r.json():
#         if x['appName'] in list(seg_list):
#
#
#             # return ret[0]


# 只监控指定群
@bot.register([group], TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if not (isinstance(msg.chat, Group) and not msg.is_at):
        # seg_list = jieba.cut(msg.text, cut_all=False)
        # print('/'.join(seg_list))
        for x in r.json():
            if x['appName'] in ['全市通办']:
                ludareply.do_reply(msg)


# 堵塞线程，并进入 Python 命令行
embed()
