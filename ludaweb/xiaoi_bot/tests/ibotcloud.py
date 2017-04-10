# -*- coding: utf-8 -*-

import unittest
import xiaoi.ibotcloud
import hashlib


class TTSTests(unittest.TestCase):
    def test_TTSParams(self):
        tts_params = xiaoi.ibotcloud.TTSParams()

        self.assertTrue(tts_params.url == "")
        self.assertTrue(tts_params.aue == "speex-wb;7")
        self.assertTrue(tts_params.txe == "utf-8")
        self.assertTrue(tts_params.auf == "audio/L16;rate=16000")

        tts_params = xiaoi.ibotcloud.TTSParams("my_url")
        self.assertTrue(tts_params.url == "my_url")
        self.assertTrue(tts_params.aue == "speex-wb;7")
        self.assertTrue(tts_params.txe == "utf-8")
        self.assertTrue(tts_params.auf == "audio/L16;rate=16000")

        # test setup_for_speex_wb/nb
        tts_params.setup_for_speex_wb()
        self.assertTrue(tts_params.url == "my_url")
        self.assertTrue(tts_params.aue == "speex-wb;7")
        self.assertTrue(tts_params.txe == "utf-8")
        self.assertTrue(tts_params.auf == "audio/L16;rate=16000")

        tts_params.setup_for_speex_nb()
        self.assertTrue(tts_params.url == "my_url")
        self.assertTrue(tts_params.aue == "speex-nb;7")
        self.assertTrue(tts_params.txe == "utf-8")
        self.assertTrue(tts_params.auf == "audio/L16;rate=16000")

    def test_TTSSession(self):
        # test TTSSession init
        params = xiaoi.ibotcloud.TTSParams()
        signature = xiaoi.ibotcloud.IBotSignature("myappkey", "myappsec", "my_uri")

        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.TTSSession, "test", params)
        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.TTSSession, signature, "test")

        tts_session = xiaoi.ibotcloud.RegSession(signature, params)

        # copy signature & params
        self.assertTrue(tts_session.signature != signature and tts_session.params != params)

        # test get_tts_result(self, speex_data)
        test_key = "XRg2TM9Ad1tT"
        test_sec = "g1PLtSFBadd3xNJYqulU"
        params = xiaoi.ibotcloud.TTSParams(url="http://vcloud.xiaoi.com/synth.do")


        signature = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                                  app_sec=test_sec,
                                                  uri="/synth.do",
                                                  http_method="POST")

        tts_session = xiaoi.ibotcloud.TTSSession(signature, params)
        ret = tts_session.get_tts_result("你好")

        self.assertTrue(ret.http_status == 200)
        self.assertTrue(len(ret.http_body) == 2135)


class RegTests(unittest.TestCase):
    def test_RegSession(self):
        # test RegSession init
        params = xiaoi.ibotcloud.RegParams()
        signature = xiaoi.ibotcloud.IBotSignature("myappkey", "myappsec", "my_uri")

        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.RegSession, "test", params)
        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.RegSession, signature, "test")

        reg_session = xiaoi.ibotcloud.RegSession(signature, params)

        # copy signature & params
        self.assertTrue(reg_session.signature != signature and reg_session.params != params)

        # test get_reg_result(self, speex_data)
        test_key = "XRg2TM9Ad1tT"
        test_sec = "g1PLtSFBadd3xNJYqulU"
        params = xiaoi.ibotcloud.RegParams(url="http://vcloud.xiaoi.com/recog.do")



        signature = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                                  app_sec=test_sec,
                                                  uri="/recog.do",
                                                  http_method="POST")

        params.setup_for_speex_wb()

        reg_session = xiaoi.ibotcloud.RegSession(signature, params)

        # set current work directory iCloudSDK/tests
        speex_data = open("../data/test16k.spx", "rb").read()

        self.assertTrue(len(speex_data) == 2135)

        ret = reg_session.get_reg_result(speex_data)

        self.assertTrue(ret.http_status == 200)
        self.assertTrue(ret.http_body == "你好")

    def test_RegParams(self):
        # test RegParams init
        reg_params = xiaoi.ibotcloud.RegParams()

        self.assertTrue(reg_params.url == "")
        self.assertTrue(reg_params.aue == "speex-wb;7")
        self.assertTrue(reg_params.txe == "utf-8")
        self.assertTrue(reg_params.auf == "audio/L16;rate=16000")

        reg_params = xiaoi.ibotcloud.RegParams("my_url")
        self.assertTrue(reg_params.url == "my_url")
        self.assertTrue(reg_params.aue == "speex-wb;7")
        self.assertTrue(reg_params.txe == "utf-8")
        self.assertTrue(reg_params.auf == "audio/L16;rate=16000")

        # test setup_for_speex_wb/nb
        reg_params.setup_for_speex_wb()
        self.assertTrue(reg_params.url == "my_url")
        self.assertTrue(reg_params.aue == "speex-wb;7")
        self.assertTrue(reg_params.txe == "utf-8")
        self.assertTrue(reg_params.auf == "audio/L16;rate=16000")

        reg_params.setup_for_speex_nb()
        self.assertTrue(reg_params.url == "my_url")
        self.assertTrue(reg_params.aue == "speex-nb;7")
        self.assertTrue(reg_params.txe == "utf-8")
        self.assertTrue(reg_params.auf == "audio/L16;rate=16000")



class AskTests(unittest.TestCase):
    def test_AskSession(self):
        # test AskSession init
        params = xiaoi.ibotcloud.AskParams()
        signature = xiaoi.ibotcloud.IBotSignature("myappkey", "myappsec", "my_uri")

        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.AskSession, "test", params)
        self.failUnlessRaises(TypeError, xiaoi.ibotcloud.AskSession, signature, "test")

        ask_session = xiaoi.ibotcloud.AskSession(signature, params)

        # copy signature & params
        self.assertTrue(ask_session.signature != signature and ask_session.params != params)

        # test get_answer(self, question)
        test_key = "XRg2TM9Ad1tT"
        test_sec = "g1PLtSFBadd3xNJYqulU"
        params = xiaoi.ibotcloud.AskParams(platform="custom",
                                           user_id="abc",
                                           url="http://nlp.xiaoi.com/ask.do",
                                           response_format="xml")

        # test AskParam - __str__


        signature = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                                  app_sec=test_sec,
                                                  uri="/ask.do",
                                                  http_method="POST")

        ask_session = xiaoi.ibotcloud.AskSession(signature, params)

        ret = ask_session.get_answer("你好")

        self.assertTrue(ret.http_status == 200)
        self.assertTrue(ret.http_body != "")

    def test_AskParams(self):
        # test AskParams init
        ask_params = xiaoi.ibotcloud.AskParams()

        self.assertTrue(ask_params.platform == "")
        self.assertTrue(ask_params.user_id == "")
        self.assertTrue(ask_params.url == "")

        ask_params = xiaoi.ibotcloud.AskParams(platform="ios",
                                               user_id="my_id",
                                               url="http://www.google.com")

        self.assertTrue(ask_params.platform == "ios")
        self.assertTrue(ask_params.user_id == "my_id")
        self.assertTrue(ask_params.url == "http://www.google.com")

        ask_params = xiaoi.ibotcloud.AskParams("ios", "my_id", "http://www.google.com")
        self.assertTrue(ask_params.platform == "ios")
        self.assertTrue(ask_params.user_id == "my_id")
        self.assertTrue(ask_params.url == "http://www.google.com")



class IBotSignatureTests(unittest.TestCase):
    """
    It's the unittests for IBotSignature
    """

    def test_init(self):
        test_sign = xiaoi.ibotcloud.IBotSignature("myappkey", "myappsec", "my_uri")

        self.assertTrue(test_sign.app_key == "myappkey")
        self.assertTrue(test_sign.app_sec == "myappsec")
        self.assertTrue(test_sign.uri == "my_uri")
        self.assertTrue(test_sign.http_method == "POST")
        self.assertTrue(test_sign.realm == "xiaoi.com")

        test_sign = xiaoi.ibotcloud.IBotSignature("my_app_key", "my_app_sec", "my_uri", "GET", "google.com");
        self.assertTrue(test_sign.app_key == "my_app_key")
        self.assertTrue(test_sign.app_sec == "my_app_sec")
        self.assertTrue(test_sign.uri == "my_uri")
        self.assertTrue(test_sign.http_method == "GET")
        self.assertTrue(test_sign.realm == "google.com")

        test_sign = xiaoi.ibotcloud.IBotSignature("my_app_key", "my_app_sec", "my_uri", "geT", "google.com");
        self.assertTrue(test_sign.http_method == "GET")

    def test_functions(self):
        #test sha1
        test_value1 = "testkey:xiaoi.com:testsecret"
        test_value2 = "76053314351f9527a1e3565d456fc10c26052740:4d51eface1f38cd2b76c6f215d2e7b59df3v1679:3550ee8ce9ff7cd3e75c6f8f5d686b491f3b1370";

        targetRet1 = "76053314351f9527a1e3565d456fc10c26052740"
        targetRet2 = "2f33b01e91979640538a1084e068b043be63f820"

        self.assertTrue(hashlib.sha1(test_value1).hexdigest() == targetRet1)
        self.assertTrue(hashlib.sha1(test_value2).hexdigest() == targetRet2)

        test_sign = xiaoi.ibotcloud.IBotSignature("my_app_key", "my_app_sec", "my_uri", "geT", "google.com");
        vals = test_sign.get_signature()

        self.assertTrue(vals.signature)
        self.assertTrue(vals.nonce)

        self.assertTrue(test_sign.get_http_header_xauth());

if __name__ == "__main__":
    unittest.main()


