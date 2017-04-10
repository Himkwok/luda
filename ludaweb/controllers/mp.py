# -*- coding: utf-8 -*-
import hashlib
from ludaweb import app
from flask import make_response, request
import xml.etree.ElementTree as ET
import time
from ludaweb.xiaoi_bot.xiaoi import ibotcloud
import requests
from ludaweb.models.applications import Application

test_key = "ujr4acjvzXNA"
test_sec = "9lghG7BDzv1ggMZ1CkzU"
signature_ask = ibotcloud.IBotSignature(app_key=test_key, app_sec=test_sec, uri="/ask.do", http_method="POST")
params_ask = ibotcloud.AskParams(platform="custom", user_id="abc", url="http://nlp.xiaoi.com/ask.do",
                                 response_format="xml")

ask_session = ibotcloud.AskSession(signature_ask, params_ask)


@app.endpoint('webhook')
def mphook():
    applist = ['全市通办']
    if request.method == 'GET':
        token = '69b3f633cd9e4136bfdd8be812a34e28'  # 微信配置所需的token
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s).encode()
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        app.logger.error(xml_rec.find('Content').text)
        content = xml_rec.find('Content').text + " -- from luda"
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

        xml_rep_mutiimg = '''<xml>
                                <ToUserName><![CDATA[%s]]></ToUserName>
                                <FromUserName><![CDATA[%s]]></FromUserName>
                                <CreateTime>%s</CreateTime>
                                <MsgType><![CDATA[news]]></MsgType>
                                <ArticleCount>1</ArticleCount>
                                <Articles>
                                    <item>
                                        <Title><![CDATA[%s]]></Title>
                                        <Description><![CDATA[%s]]></Description>
                                        <PicUrl><![CDATA[%s]]></PicUrl>
                                        <Url><![CDATA[%s]]></Url>
                                    </item>                                    
                                </Articles>
                            </xml>'''
        if xml_rec.find('Content').text in applist:
            app.logger.error(xml_rec.find('Content').text + " is in the applist...")
            home_title = '您好\n' + "以下是您所属分局的全市通办统计情况:"
            my_imag_url = "http://47.92.37.219/static/img/234979-1404251G15249.jpg"
            application = Application.query.filter_by(id=3).first()
            ret = requests.post(application.url, data={})
            returnList = ret.json()['result']

            det = []
            count = []
            for ret in returnList:
                if '上海市徐汇区税务局' == ret['yyslfjmc']:
                    count.append(ret['jjqphj'])
                    count.append(ret['qthj'])
                    det.append(".%s:%s笔，发票申领%s笔，其他%s笔\n" % (
                        ret['nsrzgfjmc'], str(ret['jjqphj'] + ret['qthj']), str(ret['jjqphj']), str(ret['qthj'])))

            des = "截止%s,共收到外区申请事项%s笔，其中\n" % (time.strftime("%Y-%m-%d", time.localtime(time.time())), str(sum(count)))

            response = make_response(xml_rep_mutiimg % (
                fromu, tou, str(int(time.time())), home_title, des + ''.join(det), my_imag_url,
                "http://47.92.37.219/qstb/3"))
            response.content_type = 'application/xml'
            return response
        else:
            ret_ask = ask_session.get_answer(xml_rec.find('Content').text)
            response = make_response(xml_rep % (fromu, tou, str(int(time.time())), ret_ask.http_body.decode()))
            response.content_type = 'application/xml'
            return response
    return 'Hello weixin!'
