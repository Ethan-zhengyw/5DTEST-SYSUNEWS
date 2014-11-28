#-*- coding: utf-8 -*-
"""Module to process database
"""
import os
import re
import os.path
import urllib
import MySQLdb

import api

con = MySQLdb.connect(
    host="localhost",
    user="sysunews",
    passwd="sysunews",
    db="sysunewsDB",
    charset="utf8"
)

cursor = con.cursor()

hostIP = os.popen('ifconfig | grep inet | grep -v inet6 | grep -v 127 | cut -d ":" -f 2 | cut -d " " -f 1').read()[:-1]

def save_urls(urls):
    """Save the urls into database

    Note:
        When url is already in database, it will just ignore it quietly

    Args:
        urls (list): url list

    """
    #print " saving urls into sysunewsDB.urls...\n+------------------------------------"
    count = 0
    length = len(urls)

    for url in urls:
        if check_news(api.get_newsid(url)):
            continue
        count = count + 1

        newsid = api.get_newsid(url)
        module = api.get_module(url)
        param = [newsid, module, url]

        #print " saving url " + str(count) + "/" + str(length) + ": " + url
        cursor.execute('insert into urls values(%s, %s, %s)', param)

    con.commit()
    #print "+------------------------------------\n Finished ", count, "new url fetched!\n"


def save_news(news):
    """Save news into database

    Note:
        Will check whether the news is already in database
    
    Args:
        news (dict): a news dictionary 

    """
    if check_news(api.get_newsid(news["url"])):
        return

    print " saving news: " + news["url"] + " " + news["h1"]

    pattern = '('
    pattern_sql = '('
    param = []

    for attr in news:
        attr_str = str(news[attr])
        if attr == "imgs" and len(news["imgs"]) != 0:
            for img_url in news["imgs"]:
                print "saving img", img_url
                save_img(img_url)

        if attr in ["newsid", "module", "visit_times"]:
            attr_str = int(attr_str)
        param.append(attr_str)

        pattern = pattern + '%s, '
        attr_db = (attr if attr != "div" else "maindiv")
        pattern_sql = pattern_sql + attr_db + ', '

    pattern_sql = pattern_sql[:-2] + ')'
    pattern = 'insert into news' + pattern_sql + ' values' + pattern[:-2] + ')'

    cursor.execute(pattern, param)
    save_urls([news["url"]])
    con.commit()


def save_img(url):
    """Save the image

    Note:
        the images will be save in directory /home/images/
        and it will check whether it's already exists

    Args:
        url (str): the url of the image, like [images/content/2014-11/20141124172306071544.jpg]

    """
    dirname = '/home/' + url[:url.rfind('/')]
    filename = '/home/' + url

    if not os.path.isfile(filename):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        try:
            image = open(filename, 'wb')
            image.write(urllib.urlopen('http://news2.sysu.edu.cn/' + url).read())
            image.close()
        except:
            pass


def check_news(tablename, newsid):
    """Check whether the news already exist

    Can do this in two different ways: refer to table urls or news

    Args:
        tablename (str): 

    Return:
        bool: return true if find new with the same newsid in database else return False

    """
    cursor.execute('select newsid from ' + tablename + ' where newsid = %s', newsid)
    result = cursor.fetchone()

    return (True if result else False)


def cleandb():
    """Clean the database

    This fuction will delete two table: urls and news in sysunewsDB

    """
    cursor.execute('truncate table urls')
    cursor.execute('truncate table news')
    con.commit()


def get_news(module, start, num):
    """Query data from database

    When querying news from DB, the news will be return according to the order of update time, which means the start 1 is the newest news

    Args:
        module (int): find news from which module
        start (int): the start index in DB
        num (int): how many news want to get

    Returns:
        list: a list of news, every news is a dictionary

    """
    patterns = ["newsid", "module", "visit_times", "date", "url", "imgs", "author", "editor", "h1", "h2", "source", "maindiv"]
    result = []

    sql = 'select * from news where module=' + str(module) + " order by date desc"

    if start != 0 and num != -1:
        sql = sql + ' limit ' + str(start - 1) + ',' + str(num)

    cursor.execute(sql)
    
    for item in cursor.fetchall():
        count = 0
        news = {}

        for attr in item:
            news[patterns[count]] = attr
            count = count + 1

        result.append(news)

    patterns = ['\r', '\n', '\t', 'NULL']

    for news in result:
        for pattern in patterns:
            news["maindiv"] = news["maindiv"].replace(pattern, "")

        news["maindiv"] = re.sub(u'阅读次数：<script.*?/script>', u'阅读次数：' + str(news["visit_times"]), news["maindiv"])
        #news["maindiv"] = re.sub('/home/sysunews/images', "/home/images", news["maindiv"])
        #news["maindiv"] = re.sub('(?<!home)/images', "/home/images", news["maindiv"])
        #news["maindiv"] = re.sub('../home/images', "/home/images", news["maindiv"])
        news["maindiv"] = re.sub("(?<=src).*/images", "=\"/home/images", news["maindiv"])

    return result


def check_news(newsid):
    """Check whether the news already exist in table urls

    Args:
        tablename (str): 

    Return:
        bool: return true if find new with the same newsid in table urls else return False

    """
    sql = 'select * from urls where newsid=' + str(newsid)
    cursor.execute(sql)
    for item in cursor.fetchall():
        for attr in item:
            if str(newsid) == str(attr):
                return True

    return False


def get_module_newsNum(module):
    """get the num of news is certain module

    Args:
        module (int): find news number of which module

    Returns:
        int: the number of news of certain module in database

    """
    sql = 'select count(newsid) from urls where module=' + str(module)
    cursor.execute(sql)
    for item in cursor.fetchall():
        for attr in item:
            return attr

    return 0
