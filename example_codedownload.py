#!/usr/bin/env python
from luogu import *
from bs4 import BeautifulSoup

import asyncio
import os
import ssl

cookie = 'UM_distinctid=1628f18d8fa568-0c77f61d2d6685-336c7b05-100200-1628f18d8fb74e; __client_id=4481c1bb80e250e3e1b43eb658c1f4882b4c98a5; CNZZDATA5476811=cnzz_eid%3D657620256-1522818985-%26ntime%3D1528115158'
ID = 72813  # 这里写你的id
mainUrl = 'https://www.luogu.org'
pageUrl = 'https://www.luogu.org/recordnew/lists?uid=' + str(ID) + '&page='
downloadPath = 'download/'
codePath = downloadPath + 'code/'

DEBUG = True

# browser
browser = LuoguBrowser()
browser.insert_headers('cookie', cookie)


def getPageUrl(pageNum):
    return pageUrl + str(pageNum)


def saveLocal(fileName, text):
    path = codePath + fileName + '.cpp'
    if os.path.exists(path):
        return
    f = open(path, mode='w')
    f.write(text)
    f.close()


def downloadCode(url):
    browser.openURL(url)
    data = browser.getData()
    html = browser.ungzip(data).decode()
    soup = BeautifulSoup(html, 'html.parser')
    try:
        text = soup.find('code').get_text()
        name = soup.find('h1').get_text()
        saveLocal(name, text)
        print('下载完成:%s' % url)
        return True
    except AttributeError:
        print('下载异常:%s' % url)
        return False


def searchPage(start, end):
    """ [start, end)
    """
    count = 0
    for i in range(start, end):
        if DEBUG:
            print("现在是第%d页" % i)
        url = getPageUrl(i)
        browser.openURL(url)
        data = browser.getData()
        html = browser.ungzip(data).decode()
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('div', {
            'class': 'lg-content-table-left'
        }).find_all('div', {'class': 'am-g lg-table-bg0 lg-table-row'})
        for item in items:
            point = item.find('strong', {'class': 'lg-fg-green'})
            if point is None:
                continue
            acurl = item.find_all('a', {
                'target': '_blank',
                'data-pjax': ''
            })[0]['href']
            import re
            if re.search(acurl, '/record/show?rid=*'):
                if DEBUG:
                    print(acurl)
                continue
            if downloadCode(mainUrl + acurl):
                count += 1
    print('代码共', count)


def main():
    page = 1  # start Page
    url = getPageUrl(page)
    browser.openURL(url)
    data = browser.getData()
    html = browser.ungzip(data).decode()
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('ul', {
        'class': 'am-pagination am-pagination-centered'
    }).find_all('li')
    lastestItem = items[-1]
    maxPage = lastestItem.find('a')['data-ci-pagination-page']
    # 找到最大页码
    print('最大页数', maxPage)
    searchPage(1, int(maxPage) + 1)


def init():
    print('初始化中')
    if not os.path.exists(downloadPath):
        print('正在创建文件夹download...')
        os.makedirs(downloadPath)
        print('done...')
    if not os.path.exists(codePath):
        print('正在创建task文件')
        os.makedirs(codePath)
        print('done...')
    print('初始化完成')


if __name__:
    ssl._create_default_https_context = ssl._create_unverified_context
    init()
    main()