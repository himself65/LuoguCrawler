#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3  # 数据库
import gc
import urllib3
import multiprocessing  # 多线程模块
import threading  # 多线程模块
import ssl
import re  # 正则表达式

from time import time
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
__email__ = 'himself6565@gmail.com'

# SETTINGS
DATABASE = {
    'name': 'himself65',
}
Threads_Number = 10  # 默认10个爬虫列队
DEBUG = True

# END

GET_TASKS_SQL = '''SELECT ID FROM TASK;'''


def get_database():
    """获取数据库"""
    name = DATABASE['name'] + '.db'
    database = sqlite3.connect(name)
    return database


def task_producer(a, b):
    """生成任务 区间[a, b]"""
    db = get_database()
    cursor = db.cursor()
    for i in range(a, b + 1):
        create_task_sql = '''INSERT INTO TASK(ID)
                        VALUES (%d);''' % (i)
        cursor.executescript(create_task_sql)
    db.close()


def get_task(task_que: Queue):
    """任务队列，从数据库中加载任务放到task_que中"""
    db = get_database()
    cursor = db.cursor()
    cursor.execute(GET_TASKS_SQL)
    task_list = cursor.fetchall()
    if len(task_list) != 0:
        for item in task_que:
            time_1 = time()
            task_que.put(item)
            print("加载任务耗时: %lf" % (time() - time_1))
    else:
        print("没有找到任务")
    db.close()


def save_task(save_que: Queue):
    """存储队列 TODO"""
    db = get_database()
    cursor = db.cursor()
    while not save_que.empty():
        item = save_que.get(timeout=5)
        uid = item['uid']
        name = item['name']
        sub_num = item['submit_num']
        ac_num = item['ac_num']
        contribute = itme['contribute']
        active = item['active']
        integral = item['integral']
        created_time = item['created_time']
        save_user_sql = '''INSERT INTO USER(ID, 
                                            NAME, 
                                            SUBMIT_NUM,
                                            AC_NUM, 
                                            CONTRIBUTE,
                                            ACTIVE,
                                            INTEGRAL,
                                            CREATED_TIME)
                            VALUES(%d %s %d %d %d %d %d %s);
                            DELETE FROM TASK WHERE ID = %d;''' % (uid, name,
                                                                  sub_num,
                                                                  ac_num,
                                                                  contribute,
                                                                  active,
                                                                  integral,
                                                                  created_time,
                                                                  uid)
        # Save
        cursor.execute(save_user_sql)
        save_que.task_done()


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
            luogu_user = {
                'uid': user_id,
                'name': user_name,
                'submit_num': submit_num,
                'ac_num': ac_num,
                'contribute': contribute,
                'active': active,
                'integral': integral,
                'created_time': created_time,
            }
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
            luogu_user = {
                'uid': user_id,
                'name': user_name,
                'submit_num': -1,
                'ac_num': -1,
                'contribute': contribute,
                'active': active,
                'integral': integral,
                'created_time': created_time,
            }
        if DEBUG:
            print(luogu_user)

        # Finished
        save_que.put(luogu_user)
        task_que.task_done()


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
                        );'''
    cursor.executescript(create_table_sql)
    create_table_sql = '''CREATE TABLE IF NOT EXISTS TASK(
                            ID INT PRIMARY KEY NOT NULL
                        );'''
    cursor.execute(create_table_sql)
    # 此处不用execute则无法获取，暂且不知道原因
    cursor.execute(GET_TASKS_SQL)
    exist_task = cursor.fetchone()
    if exist_task is None:
        print("no task exist!")
        exit()
    # Close DataBase
    db.close()


def test(tq: Queue, sq: Queue):
    """Unit Test Part"""
    init()


def main(tq: Queue, sq: Queue):
    # Create Theads
    for td_id in range(1, Threads_Number + 1):
        td = threading.Thread(target=crawler, args=(tq, sq), name=str(td_id))
        threads_list.append(td)

    for td in threads_list.index():
        td.start()

    save_td = threading.Thread(target=save_task, args=(sq), name='Save_Que')
    save_td.start()
    save_td.join()
    print('Finished')


if __name__:
    # MARK -- 参考答案：https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    ssl._create_default_https_context = ssl._create_unverified_context
    # 任务列表
    task_que = Queue()
    save_que = Queue()
    main(task_que, save_que)
