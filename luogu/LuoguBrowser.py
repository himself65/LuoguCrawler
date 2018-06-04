#!/usr/bin/python3
#-*- coding:utf-8 -*-
"""
简单的爬虫项目来访问洛谷官网
"""
from __future__ import absolute_import
from http import cookiejar
from urllib import parse, request
from bs4 import BeautifulStoneSoup
import json
import socket
import gzip

__author__ = "Himself65"
__license__ = "MIT"

defaultURL = "https://www.luogu.org"

from random import sample
user_agents = [
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
]


def get_agent():
    """
    每次随机返回一个user-agent
    """
    return sample(user_agents, 1)[0]


class LuoguBrowser(object):
    """
    """
    _headers = {}

    def __init__(self):
        """ 
        初始化访问洛谷
        """
        self._headers['user-agent'] = get_agent()
        self._headers['accept-encoding'] = "gzip, deflate, br"
        self._headers['accept-language'] = "zh,en;q=0.9,zh-CN;q=0.8,ja;q=0.7"
        self.setOpener()

    def insert_headers(self, key, value):
        """
        插入值到请求头
        每次插入后会自动setOpener
        """
        self._headers[key] = value
        self.setOpener()

    def setOpener(self):
        """ 初始化opener
        """
        cj = cookiejar.CookieJar()
        pro = request.HTTPCookieProcessor(cj)
        self.opener = request.build_opener(pro)
        header = []
        for key, value in self._headers.items():
            elem = (key, value)
            header.append(elem)
        self.opener.addheaders = header

    def openURL(self, url, data=None, timeout=None):
        """
        访问地址
        """
        import socket
        if timeout is None:
            timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        if url is None:
            raise AttributeError('url is none')
        # url = url.encode('UTF8', errors='strict')
        self.response = self.opener.open(url, data=data, timeout=timeout)

    def getData(self):
        """
        获取response内容
        """
        return self.response.read()

    def getResponse(self):
        """
        获取response
        """
        return self.response

    @staticmethod
    def create_query_string_message(dictionary):
        """
        创建请求地址
        Args:
            dictionary -> 字典，例如：
            
        Returns -> String
            例如: 
            { 
                "id": 761282619,
                "name": "himself65" 
            }
            Return -> "id=761282619&name=himself65"
        """
        s = ""
        for (key, value) in dictionary.items():
            s = s + str(key) + "=" + str(value) + "&"
        return s.rstrip("&")

    @staticmethod
    def getDataFromResponse(response, data='more'):
        """
        获取response请求中特定内容
        Args:
            response -> Response
            data -> String, 需要获得的数据，默认为'more'
        Returns -> String
        """
        messages = json.loads(response)
        return messages[data]

    @staticmethod
    def check_Accessible(data, name='code', accessStatus=200):
        """
        检查状态值是否成功
        Args:
            data -> Dictionary, 为Response返回的请求
        Returns -> Bool

        """
        data_json = json.loads(data)
        return data_json[name] == accessStatus if True else False

    @staticmethod
    def ungzip(data):
        """
        ungzip the data
        """
        try:
            ungzipData = gzip.decompress(data)
        except:
            print("解压失败，返回原数据")
            return data
        return ungzipData
