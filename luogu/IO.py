#!/usr/bin/python3
#-*- coding:utf-8 -*-
"""
读写文件部分
"""
from __future__ import absolute_import

import os
import json


def saveToFile(fileLocation, content):
    """
    保存内容到指定目录
    """
    if fileLocation == None:
        raise AttributeError("fileLocation not found")
    f = open(fileLocation, mode='w')
    f.write(content)
    f.close()


def getJson(fileLocation='config.json'):
    """
    获取Json文件内容，并转义到字典
    """
    datas = open(fileLocation, mode='r')
    datas = json.loads(datas.read())
    return datas