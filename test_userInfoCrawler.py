#!/usr/bin/env python
from lowgu import *
from openpyxl import Workbook
from bs4 import BeautifulSoup
from time import time
from urllib import request
from queue import Queue

import queue
import os
import ssl
import json
import threading
import multiprocessing

defaultURL = "https://www.luogu.org"
userURL = "https://www.luogu.org/space/show?uid="

event = multiprocessing.Event()
event.set()


def download_img(url, userName):
    """ 下载图片到download/文件夹下
    """
    loc = 'download/' + userName + '.png'
    if os.path.exists(loc):
        return
    try:
        # 下载图片
        request.urlretrieve(url, filename=loc)
    except:
        print("\n404")


def crawler(begin, end, que):
    """ [begin, end)
    """
    for i in range(begin, end):
        try:
            # Get messageURL
            messageURL = userURL + str(i)
            # Init browser
            browser = LowguBrowser()
            ## View Web
            browser.openURL(messageURL)
            ## getData
            html = browser.getData()
            html = LowguBrowser.ungzip(html)
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup)
            board = soup.find(
                'ul', {'class': 'am-list am-list-static lg-summary-list'})

            items = board.find_all("li")
            # 0
            userName = soup.find('span', {'name': 'username'}).get_text()
            avatar = items[0].find('img')['src']
            # 1
            allPost = items[1].find_all('span', {'class': 'lg-bignum-num'})
            Num = allPost[0].get_text()
            ACNum = allPost[1].get_text()
            # 2
            Acts = items[4].find('span', {'class': 'lg-right'}).get_text()
            Acts = Acts.split('/')
            contribute = Acts[0]
            active = Acts[1]
            integral = Acts[2]
            # 3
            Type = items[5].find('span', {'class': 'lg-right'}).get_text()
            # 4
            registeredTime = items[6].find('span', {
                'class': 'lg-right'
            }).get_text()
            # download image
            t = [
                i, userName, avatar, Num, ACNum, contribute, active, integral,
                Type, registeredTime
            ]
            # 下载图片
            download_img(avatar, str(i))
            que.put(t)
            # print("放到队列中：", i)
        except:
            que.put([i, '???'])
            continue


def saveThread(que, sheet):
    thread = threading.current_thread()
    while thread.isAlive():
        try:
            t = que.get(block=True, timeout=60)
            sheet.append(t)
        except queue.Empty:
            thread.is_alive = False
            break
        que.task_done()
        size = que.qsize()
        if size > 0:
            print("还有大约任务数:", size, flush=True)


wbName = 'luogu.xlsx'


def main():
    title = ['id', '名字', '头像', '总提交数', 'AC数', '贡献', '活跃', '积分', '用户类型', '注册时间']
    #
    wb = Workbook(write_only=True)
    thread = []
    # queue
    que = Queue()
    sheet = wb.create_sheet(title="luogu分析")
    sheet.append(title)
    # saveThread 保存线程
    j = 1
    len = 10000
    for i in range(1, 9):  # 线程
        begin = j
        end = j + len
        t = threading.Thread(
            target=crawler, name=str(i), args=(begin, end, que))
        thread.append(t)
        j += len
    st = threading.Thread(target=saveThread, args=(que, sheet))
    for i in range(0, 8):
        thread[i].start()
    st.start()
    for i in range(0, 8):
        thread[i].join()
    st.join()
    wb.save(wbName)


if __name__:
    # MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    ssl._create_default_https_context = ssl._create_unverified_context
    main()