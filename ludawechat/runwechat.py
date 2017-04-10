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
cf = configparser.ConfigParser()
cf.read('config/wechat.cfg')
remoteweb = cf.get('WECHAT_CONFIG', 'ROMOTE_WEB')

print('远程web地址 ' + remoteweb)


# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)
group = bot.groups().search('代号：鲁达')[0]

# 打印所有群成员
for member in group:
    print(member)

# 获取所有已经配置的应用
r = requests.get(remoteweb + '/api/applications')
print(r.json())
for app in r.json():
    jieba.suggest_freq((app['appName']), True)


ludareply = Luda()

# 只监控指定群
@bot.register([group], TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if not (isinstance(msg.chat, Group) and not msg.is_at):
        seg_list = jieba.cut(msg.text, cut_all=False)
        # print('/'.join(seg_list))
        logger.debug('/'.join(seg_list))
        for x in r.json():
            if x['appName'] in list(seg_list):
                ludareply.do_reply(msg)


# 堵塞线程，并进入 Python 命令行
embed()
