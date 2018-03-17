import urllib
import ssl
import sys
import json

import luogu
from bs4 import BeautifulSoup

# url data
defaultUrl = "https://www.luogu.org"
loginUrl = "https://www.luogu.org/login/loginpage"

# 此处是我的主页和我的洛谷id
myUrl = "https://www.luogu.org/space/show?uid=72813"
myID = 72813
#
noticeUrl = "https://www.luogu.org/space/ajax_getnotice?uid=72813&mynotice=1&page="

# header
header = {}
header[
    'user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
header['accept-encoding'] = "gzip, deflate, br"
header['accept-language'] = "zh,en;q=0.9,zh-CN;q=0.8,ja;q=0.7"


def getHtml(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getUserUrl(number, page):
    return "https://www.luogu.org/space/ajax_getnotice?uid=" + str(
        number) + "&mynotice=0&page=" + str(page)

deep = 5
userNumber = []
userUrl = []
ans = []
if __name__:
    ssl._create_default_https_context = ssl._create_unverified_context
    datas = open("cookie.json")
    data = json.loads(datas.read())
    header['cookie'] = data['cookie']
    opener = luogu.getOpener(header)
    for i in range(1, 6):  # 读取50个最近消息
        url = noticeUrl + str(i)
        # 浏览器行为，之后再包装
        op = opener.open(noticeUrl)
        data = op.read()
        data = luogu.ungzip(data)
        data = luogu.getMessage(data)
        data = luogu.gethtml(data)
        html = getHtml(data)
        items = html.find_all("li")
        for item in items:
            _href = item.find("a").get("href")
            _Url = defaultUrl + _href
            _Id = luogu.findID(_Url)
            userUrl.append(_href)  # 之后判断方便
            userNumber.append(_Id)  # @了你的用户ID
    # end notice find
    for i in range(0, len(userNumber)):
        page = 0
        while True:
            # 当无法找到message时候退出
            url = getUserUrl(userNumber[i], page)  # 获得网址
            # 浏览器行为
            op = opener.open(url)
            data = op.read()
            data = luogu.ungzip(data)
            data = luogu.getMessage(data)
            data = luogu.gethtml(data)
            html = getHtml(data)
            # 进行搜索nid
            items = html.find_all(nid=True)  #找nid
            if (len(items) == 0):
                break
            if (page > deep):  # 估计函数不超过deep深度
                break
            for item in items:
                para = item.find('p')
                content = str(para)
                if content.find(str(myID)) != -1:
                    # 此处已经找到答案
                    # 放入答案列队
                    # ans.append(content)
                    print(luogu.somethingMagic(content))
                    # print(content)
            # end
            page = page + 1
    # end search
    