# -*- coding: utf-8 -*-
# please input your key/sec
import ludaweb
from ludaweb.xiaoi_bot.xiaoi import ibotcloud

test_key = "ujr4acjvzXNA"
test_sec = "9lghG7BDzv1ggMZ1CkzU"

signature_ask = ibotcloud.IBotSignature(app_key=test_key,
                                        app_sec=test_sec,
                                        uri="/ask.do",
                                        http_method="POST")

# signature_reg = ludaweb.xiaoi_bot.xiaoi.ibotcloud.IBotSignature(app_key=test_key,
#                                                         app_sec=test_sec,
#                                                         uri="/recog.do",
#                                                         http_method="POST")
#
# signature_tts = ludaweb.xiaoi_bot.xiaoi.ibotcloud.IBotSignature(app_key=test_key,
#                                                         app_sec=test_sec,
#                                                         uri="/synth.do",
#                                                         http_method="POST")
#
# params_tts = ludaweb.xiaoi_bot.xiaoi.ibotcloud.TTSParams(url="http://vcloud.xiaoi.com/synth.do")
# params_reg = ludaweb.xiaoi_bot.xiaoi.ibotcloud.RegParams(url="http://vcloud.xiaoi.com/recog.do")
params_ask =  ibotcloud.AskParams(platform="custom",
                                                         user_id="abc",
                                                         url="http://nlp.xiaoi.com/ask.do",
                                                         response_format="xml")

ask_session =  ibotcloud.AskSession(signature_ask, params_ask)
# reg_session = ludaweb.xiaoi_bot.xiaoi.ibotcloud.RegSession(signature_reg, params_reg)
# tts_session = ludaweb.xiaoi_bot.xiaoi.ibotcloud.TTSSession(signature_tts, params_tts)

# demo how to get answer
ret_ask = ask_session.get_answer("上海天气怎么样？")

print(ret_ask.http_status, ret_ask.http_body.decode())

'''
# demo how to get reg speech using speex file
speex_data = open("data/test16k.spx", "rb").read()

ret_reg = reg_session.get_reg_result(speex_data)

print(ret_reg.http_status, ret_reg.http_body)

# defmo how to get speex audio from text
ret_tts = tts_session.get_tts_result("你好")

print (ret_tts.http_status, len(ret_tts.http_body))
'''
