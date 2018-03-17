import gzip
import http.cookiejar
import os
import ssl
import time
import json
import re
from urllib import parse, request
from bs4 import BeautifulSoup


def somethingMagic(data):
    for x in re.findall(r'<a[^>]*>[^<]*?</a>', data)
        data.lstrip(x)

def magic(data):
    pattern = re.compile(ur']*>[^<]*?')
    str = u''
    print(pattern.search(str))



def findID(data):
    return re.findall(r'(\w*[0-9]+)\w*', data)[0]


def gethtml(data):
    return data['html']


def getMessage(data):
    messages = json.loads(data)
    return messages['more']


def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("解压失败")
    return data


def getOpener(head):
    cj = http.cookiejar.CookieJar()
    pro = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def check(data):
    data = json.loads(data)
    if (data['status'] == 200):
        return True
    else:
        return False
