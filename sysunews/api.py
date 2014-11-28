#-*-encoding: utf-8-*-
"""api module, call by db_update module mainly

Function in this module mainly call function in html_extracting module to finish their job.

"""
import socket
import urllib2
import cookielib
import re
import os

import post_module
import html_extracting
import db_module

default_timeout = 10
socket.setdefaulttimeout(default_timeout)
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

#hostIP = os.popen('ifconfig | grep inet | grep -v inet6 | grep -v 127 | cut -d ":" -f 2 | cut -d " " -f 1').read()[:-1]

def get_index_range(data):
    """find the index range

    Args:
        data (str): content of [http://news2.sysu.edu.cn/news0*/index.htm]

    Returns:
        start, end: two integer, corresponding to the start and the end of index

    """

    return html_extracting.find_index_range(data)


def get_newsid_firstpage(module):
    """find the newsid

    get the newsid in the first page of three module 
    in order to check whether some new news has been post

    Args:
        module (int): module to get, range form 1 to 3

    Returns:
        a list of newsid

    """
    newsids = []

    url = 'http://news2.sysu.edu.cn/news0' + str(module) + '/index.htm'
    req = post_module.req_easy_req(url)
    result = opener.open(req).read()
    
    urls = html_extracting.find_news_urls(result, module)
    for url in urls:
        newsid = get_newsid(url)
        newsids.append(newsid)

    return newsids


def get_news_urls(module):
    """Get all urls of certain module
    
    Args:
        module (int): urls of which module to get

    Returns:
        a list of urls

    """
    urls = []

    # get index range firstly
    # http://news2.sysu.edu.cn/news01/index.htm
    req = post_module.req_get_news_urls(module)
    result = opener.open(req).read()
    start, end = get_index_range(result)

    # get urls in index.htm
    urls.extend(html_extracting.find_news_urls(result, module))

    # index1.htm to end will be crawled in the following loop
    socket.setdefaulttimeout(100)
    for i in range(int(start), int(end) + 1):
        req = post_module.req_get_news_urls(module, i)
        result = opener.open(req).read()
        urls.extend(html_extracting.find_news_urls(result, module))
    socket.setdefaulttimeout(10)

    return urls


def get_module(url):
    """Get the module id of a news from its url
    
    Args:
        url (str): news' url

    Returns:
        str: the module id

    """

    return html_extracting.find_module(url)


def get_newsid(url):
    """Get the newsid of a news from its url
    
    Args:
        url (str): news' url

    Returns:
        str: the newsid

    """

    return html_extracting.find_newsid(url)


def get_news(news_url):
    """Get a news from its url
    
    Args:
        url (str): news' url

    Returns:
        dict: a dictionary store many attrubites of the news in key-value

    """
    news = {}

    try:
        req = post_module.req_get_news(news_url)
        result = opener.open(req).read()

        news = html_extracting.find_news(result)
        news["url"] = news_url
        news["module"] = html_extracting.find_module(news_url)
        news["newsid"] = html_extracting.find_newsid(news_url)

    #except urllib2.URLError, socket.timeout:
    except:

        f = open('log','a')
        f.write("Fetch information cost too much time! ignore news: " + news_url + "\n")
        f.close()
        print " Fetch information cost too much time! ignore news:", news_url
        news = {}

    return news


def get_news_fromDB(module, start=1, num=-1):
    """Query data from database

    When querying news from DB, the news will be return according to the order of update time, which means the start 1 is the newest news

    Args:
        module (int): find news from which module
        start (int): the start index in DB
        num (int): how many news want to get

    Returns:
        list: a list of news, every news is a dictionary

    """

    patterns = ['\r', '\n', '\t', 'NULL']
    newslist = db_module.get_news(module, start, num)
    for news in newslist:
        for pattern in patterns:
            news["maindiv"] = news["maindiv"].replace(pattern, "")

        news["maindiv"] = re.sub(u'阅读次数：<script.*?/script>', u'阅读次数：' + str(news["visit_times"]), news["maindiv"])
        news["maindiv"] = re.sub('/home/sysunews/images', "/home/images", news["maindiv"])
        news["maindiv"] = re.sub('(?<!home)/images', "/home/images", news["maindiv"])

    return newslist
