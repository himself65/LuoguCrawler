"""
单元测试部分
"""
from luogu import LuoguBrowser, IO

import ssl

defaultURL = "https://www.luogu.org"


def BrowserDefaultTest():
    """
    单元测试部分
    测试内容：LuoguBrowser是否可以正常使用
    """
    # MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    ssl._create_default_https_context = ssl._create_unverified_context
    # Init browser
    browser = LuoguBrowser()
    ## View Web
    browser.openURL(defaultURL)
    ## getData
    data = browser.getData()
    data = LuoguBrowser.ungzip(data)
    print(data)


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