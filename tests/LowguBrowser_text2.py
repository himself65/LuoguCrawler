#!/usr/bin/env python

from lowgu import *

import ssl
import json


def getCookie(name="cookie.json"):
    datas = open(name)
    datas = json.loads(datas.read())
    return datas['cookie']


defaultURL = "https://www.luogu.org"
mySpaceNoticeURL = "https://www.luogu.org//space/ajax_getnotice?"
myNoticeURL = "https://www.luogu.org/space/ajax_getnotice?uid=72813&mynotice=1&page="
AcInf = {"uid": "72813", "mynotice": 1, "page": 1}

userNumber = []
userUrl = []

# MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

# Get messageURL
messageURL = mySpaceNoticeURL + LowguBrowser.create_query_string_message(AcInf)
# Init browser
browser = LowguBrowser()
## Add Cookie
cookie = getCookie()
browser.insert_headers('cookie', cookie)
## View Web
browser.openURL(messageURL)
## getData
data = browser.getData()
data = LowguBrowser.ungzip(data)
if LowguBrowser.check_Accessible(data):
    print("Access")
    