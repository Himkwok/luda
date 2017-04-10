# -*- coding: utf-8 -*-
import datetime
import hashlib
import copy
#import httplib, urllib, urlparse
import requests
import collections

__author__ = 'peter.liu@xiaoi.com'


class AskParams:
    def __init__(self, platform="", user_id="", url="", response_format="json"):
        self.platform = platform
        self.user_id = user_id
        self.url = url
        self.response_format = response_format

    def __str__(self):
        return "platform:" + self.platform + "\n" + \
               "user_id:" + self.user_id + "\n" + \
               "url:" + self.url + "\n" + \
               "format:" + self.response_format


class AskSession:
    def __init__(self, signature, params):
        if not isinstance(signature, IBotSignature):
            raise TypeError("signature should be IBotSignature")

        if not isinstance(params, AskParams):
            raise TypeError("params should be AskParams")

        self.signature = copy.copy(signature)
        self.params = copy.copy(params)

    def get_answer(self, question):
        http_params ={'question': question,
                                        'format': self.params.response_format,
                                        'platform': self.params.platform,
                                        'userId': self.params.user_id}

        xauth = self.signature.get_http_header_xauth()

        http_headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain",
                        list(xauth.keys())[0]: list(xauth.values())[0]}

        url = self.params.url

        # conn = httplib.HTTPConnection(url.netloc)
        # conn.request("POST", url.path, http_params, http_headers)
        # response = conn.getresponse()

        r = requests.post(url, data=http_params,headers=http_headers)

        ret = collections.namedtuple("get_answer_return", "http_status http_body")

        ret.http_body = r.content
        ret.http_status = r.status_code
        #
        # conn.close()

        return ret


class RegParams:
    def __init__(self, url=""):
        self.aue = ""
        self.txe = ""
        self.auf = ""
        self.url = url

        self.setup_for_speex_wb()

    def setup_for_speex_wb(self):
        self.aue = "speex-wb;7"
        self.txe = "utf-8"
        self.auf = "audio/L16;rate=16000"

    def setup_for_speex_nb(self):
        self.aue = "speex-nb;7"
        self.txe = "utf-8"
        self.auf = "audio/L16;rate=16000"

    def __str__(self):
        return "aue:" + self.aue + "\n" + \
               "txe:" + self.txe + "\n" + \
               "auf:" + self.auf + "\n" + \
               "url:" + self.url


class RegSession:
    def __init__(self, signature, params):
        if not isinstance(signature, IBotSignature):
            raise TypeError("signature should be IBotSignature")

        if not isinstance(params, RegParams):
            raise TypeError("params should be RegParams")

        self.signature = copy.copy(signature)
        self.params = copy.copy(params)

    def get_reg_result(self, speex_data):
        xauth = self.signature.get_http_header_xauth()

        http_headers = {"Content-type": "application/audio",
                        "Accept": "text/plain",
                        "X-AUE": self.params.aue,
                        "X-TXE": self.params.txe,
                        "X-AUF": self.params.auf,
                        list(xauth.keys())[0]: list(xauth.values())[0]}

        url = self.params.url

        #conn = httplib.HTTPConnection(url.netloc)
        #conn.request("POST", url.path, speex_data, http_headers)
        #response = conn.getresponse()
        response = requests.post(url, data=speex_data, headers=http_headers)

        ret = collections.namedtuple("get_reg_result_return", "http_status http_body")

        ret.http_body = response.content
        ret.http_status = response.status_code

        # conn.close()

        return ret


class TTSParams(RegParams):
    def __init__(self, url=""):
        RegParams.__init__(self, url)


class TTSSession:
    def __init__(self, signature, params):
        if not isinstance(signature, IBotSignature):
            raise TypeError("signature should be IBotSignature")

        if not isinstance(params, TTSParams):
            raise TypeError("params should be TTSParams")

        self.signature = copy.copy(signature)
        self.params = copy.copy(params)

    def get_tts_result(self, tts_string):
        xauth = self.signature.get_http_header_xauth()

        http_headers = {"Content-type": "text/plain",
                        "X-AUE": self.params.aue,
                        "X-TXE": self.params.txe,
                        "X-AUF": self.params.auf,
                        list(xauth.keys())[0]: list(xauth.values())[0]}

        url =  self.params.url

        #conn = httplib.HTTPConnection(url.netloc)
        #conn.request("POST", url.path, tts_string, http_headers)
        #response = conn.getresponse()
        response = requests.post(url, data=tts_string, headers=http_headers)
        ret = collections.namedtuple("get_tts_result_return", "http_status http_body")

        ret.http_body = response.content
        ret.http_status = response.status_code

        #conn.close()

        return ret


class IBotSignature:
    """
        It's about iBotCloud signature stuff
    """

    def __init__(self, app_key, app_sec, uri, http_method="POST", realm="xiaoi.com"):
        self.app_key = app_key
        self.app_sec = app_sec
        self.uri = uri
        self.http_method = http_method.upper()
        self.realm = realm

    def get_signature(self):
        time_str = str(datetime.datetime.now()).encode('utf-8')
        nonce = hashlib.sha1(time_str).hexdigest()

        HA1 = "{0}:{1}:{2}".format(self.app_key, self.realm, self.app_sec)
        HA1 = hashlib.sha1(HA1.encode('utf-8')).hexdigest()

        HA2 = "{0}:{1}".format(self.http_method, self.uri)
        HA2 = hashlib.sha1(HA2.encode('utf-8')).hexdigest()

        signature = "{0}:{1}:{2}".format(HA1, nonce, HA2)
        signature = hashlib.sha1(signature.encode('utf-8')).hexdigest()

        # print "signature:" + signature
        # print "nonce:" + nonce
        ret = collections.namedtuple("get_signature_reture", "signature nonce")

        ret.signature = signature
        ret.nonce = nonce

        return ret

    def get_http_header_xauth(self):
        ret_vals = self.get_signature()

        ret = {'X-Auth': "app_key=\"{0}\",nonce=\"{1}\",signature=\"{2}\"".format(self.app_key,
                                                                                  ret_vals.nonce,
                                                                                  ret_vals.signature)}

        return ret




