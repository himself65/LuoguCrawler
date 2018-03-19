#!/usr/bin/env python

from lowgu import *

import ssl
import json


def getCookie(name="cookie.json"):
    datas = open(name)
    datas = json.loads(datas.read())
    datas.close()
    return datas['cookie']


defaultURL = "https://www.luogu.org"

userNumber = []
userUrl = []

# MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

browser = LowguBrowser()
cookie = getCookie()
browser.insert_headers('cookie', cookie)
browser.openURL(defaultURL)
data = browser.getData()
print(data)