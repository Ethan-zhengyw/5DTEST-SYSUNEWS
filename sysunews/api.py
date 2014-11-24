#-*-encoding: utf-8-*-
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

hostIP = os.popen('ifconfig | grep inet | grep -v inet6 | grep -v 127 | cut -d ":" -f 2 | cut -d " " -f 1').read()[:-1]

def get_index_range(data):
    return html_extracting.find_index_range(data)


# get the newsid in the first page of three module 
# in order to check whether some new news has been post
def get_newsid_firstpage(module):
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

    return html_extracting.find_module(url)


def get_newsid(url):

    return html_extracting.find_newsid(url)


def get_news(news_url):
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


#  Following function will query data from database
# --------------------------
def get_news_fromDB(module, start=1, num=-1):

    patterns = ['\r', '\n', '\t', 'NULL']
    newslist = db_module.get_news(module, start, num)
    for news in newslist:
        for pattern in patterns:
            news["maindiv"] = news["maindiv"].replace(pattern, "")

        news["maindiv"] = re.sub(u'阅读次数：<script.*?/script>', u'阅读次数：' + str(news["visit_times"]), news["maindiv"])
        news["maindiv"] = re.sub('/home/sysunews/images', "/home/images", news["maindiv"])
        news["maindiv"] = re.sub('(?<!home)/images', "/home/images", news["maindiv"])

    return newslist
