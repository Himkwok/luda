from selenium import webdriver
from selenium.webdriver import PhantomJS
import datetime
import hashlib
import os
import subprocess
import uuid

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(APP_ROOT, 'static')
MEDIA_URL = '/static/'

PASSWORD = 'shh'
PHANTOM = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'screenshot.js')


class DoCapture(object):
    '''访问URL并截取屏幕保存'''
    def do_capture(url):
        # print(url)
        url_hash = str(uuid.uuid4())  # hashlib.md5(url.encode()).hexdigest()
        filename = 'ludaweb-%s.jpg' % url_hash
        outfile = os.path.join(MEDIA_ROOT, filename)
        params = [PHANTOM, SCRIPT, url, outfile]
        # print(params)
        exitcode = subprocess.call(params)
        if exitcode == 0:
            return os.path.join(MEDIA_URL, filename)
