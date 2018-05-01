"""
单元测试部分
"""
from luogu import LuoguBrowser, IO

import ssl

defaultURL = "https://www.luogu.org"
mySpaceNoticeURL = "https://www.luogu.org//space/ajax_getnotice?"
myNoticeURL = "https://www.luogu.org/space/ajax_getnotice?uid=72813&mynotice=1&page="
AcInf = {"uid": "72813", "mynotice": 1, "page": 1}


def BrowserDefaultTest():
    """
    单元测试部分
    测试内容：LuoguBrowser是否可以正常使用，通过向空间通知发送消息
    需求：将cookie.js文件补全
    """
    userNumber = []
    userUrl = []
    # MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    ssl._create_default_https_context = ssl._create_unverified_context

    # Get messageURL
    messageURL = mySpaceNoticeURL + LuoguBrowser.create_query_string_message(
        AcInf)
    # Init browser
    browser = LuoguBrowser()
    ## Add Cookie
    cookie = IO.getJson()['cookie']
    browser.insert_headers('cookie', cookie)
    ## View Web
    browser.openURL(messageURL)
    ## getData
    data = browser.getData()
    data = LuoguBrowser.ungzip(data)
    print(data)
    if LuoguBrowser.check_Accessible(data):
        print("Access")


def OITest():
    """
    OI部分测试
    """
    json = IO.getJson()
    print(json)
    print(json['cookie'])


def main():
    print('BrowserDefaultTest is Running...')
    BrowserDefaultTest()
    print('BrowserDefaultTest Sucess!')

    print('OITest is Running...')
    OITest()
    print('OITest Sucess')


if __name__:
    main()