#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import gc
import pika
import urllib3
import multiprocessing
import threading
import ssl
import re  # 正则表达式

from queue import Queue
from bs4 import BeautifulSoup
from luogu import LuoguBrowser
"""
重构洛谷用户数据爬取
多进程爬虫 + 数据库存储 + 缓存机制 + 内存优化

过程：
    1.消息列队发送任务
    2.爬虫列队抓取网页分析
    3.保存列队保存到本地
"""
__author__ = 'himself65'
__license__ = 'MIT'

DATABASE = {
    'name': 'himself65',
}

DEBUG = True


def task_producer(a, b):
    """生成任务 区间[a, b]"""
    db_name = DATABASE['name']
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    for i in range(a, b + 1):
        create_task_sql = '''INSERT INTO TASK(ID)
                        (%d);''' % (i)
        cursor.executescript(create_task_sql)
    db.close()


def get_task(task_que: Queue):
    """任务队列 TODO"""

    pass


def save_task(save_que: Queue):
    """存储队列 TODO"""
    pass


def crawler(task_que: Queue, save_que: Queue):
    """爬虫部分"""
    import urllib
    import time
    user_url = "https://www.luogu.org/space/show?uid="

    def get_url(user_id):
        """得到用户的url"""
        return '%s%s' % (user_url, user_id)

    while not task_que.empty():
        user_id = task_que.get(block=True)
        url = get_url(user_id)
        start_time = time.time()
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        if DEBUG:
            print('用户:%d 用时%lf' % (user_id, time.time() - start_time))
        if re.match('提示', soup.title.string) is not None:
            # 判断用户是否存在
            print('不存在用户', user_id)
            continue
        """
        公开代码者有 5 个ul
            1. avatar
            2. ac_num submit_num
            3. contribute active integral
            4. utype
            5. created_time
        隐私保护者有 4 个ul
            1. avatar
            2. contribute active integral
            3. utype
            4. created_time
        """
        # 找到信息板块
        board = soup.find('ul',
                          {'class': 'am-list am-list-static lg-summary-list'})
        board_items = board.find_all("li")
        # start
        user_name = soup.find('span', {'name': 'username'}).get_text()
        if len(board_items) == 7:
            """公开代码用户"""
            # 1
            allPost = board_items[1].find_all('span',
                                              {'class': 'lg-bignum-num'})
            submit_num = allPost[0].get_text()
            ac_num = allPost[1].get_text()
            # 2
            acts = board_items[4].find('span', {
                'class': 'lg-right'
            }).get_text()
            acts = acts.split('/')
            contribute = acts[0]
            active = acts[1]
            integral = acts[2]
            # 3
            utype = board_items[5].find('span', {
                'class': 'lg-right'
            }).get_text()
            # 4
            created_time = board_items[6].find('span', {
                'class': 'lg-right'
            }).get_text()
            luogu_user = [
                user_name,
                submit_num,
                ac_num,
                contribute,
                active,
                integral,
                created_time,
            ]
            print(luogu_user)
        else:
            """隐私代码用户"""
            acts = board_items[1].find('span', {
                'class': 'lg-right'
            }).get_text()
            acts = acts.split('/')
            contribute = acts[0]
            active = acts[1]
            integral = acts[2]
            created_time = board_items[3].find('span', {
                'class': 'lg-right'
            }).get_text()
            luogu_user = [
                user_name,
                contribute,
                active,
                integral,
                created_time,
            ]
            print(luogu_user)
        if DEBUG:
            pass
            # for i, item in enumerate(board_items):
            #     print(i, item)


def get_database():
    """获取数据库"""
    name = DATABASE['name'] + '.db'
    database = sqlite3.connect(name)
    return database


def init():
    db = get_database()
    cursor = db.cursor()
    # 创建表
    create_table_sql = '''CREATE TABLE IF NOT EXISTS USER(
                            ID INT  PRIMARY KEY NOT NULL,
                            NAME TEXT     NOT NULL,
                            SUBMIT_NUM         INT,
                            AC_NUM             INT,
                            CONTRIBUTE         INT,
                            ACTIVE             INT,
                            INTEGRAL           INT,
                            CREATED_TIME       TEXT
                        );
                        CREATE TABLE IF NOT EXISTS TASK(
                            ID INT PRIMARY KEY NOT NULL
                        );'''
    check_tasks_sql = '''SELECT ID FROM TASK;'''
    user_list = '''SELECT * FROM USER'''
    cursor.executescript(create_table_sql)
    #
    cursor.executescript(check_tasks_sql)
    task_list = cursor.fetchall()
    #
    cursor.executescript(user_list)
    if len(task_list) == 0:
        print("finished!")

    # close database
    db.close()


def test(tq: Queue, sq: Queue):
    init()


def main(tq: Queue, sq: Queue):
    threads_list = []

    for td_id, info in enumerate(page_ranges_list):
        td = threading.Thread(
            target=crawler, args=(work_que, save_que), name=str(td_id))
        threads_list.append(td)

    for td in threads_list.index():
        td.start()


if __name__:
    # MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    ssl._create_default_https_context = ssl._create_unverified_context
    # 任务列表
    task_que = Queue()
    save_que = Queue()
    test(task_que, save_que)
