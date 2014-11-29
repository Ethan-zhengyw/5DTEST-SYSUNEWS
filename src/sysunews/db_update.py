#-*-encoding: utf-8-*-
import urllib2
import errno

import api
import db_module

diction = {
    1: "中大新闻",
    2: "每周聚焦",
    3: "媒体中大"
}

def initial():
    """Initialize the database

    ::
    This function will get all possible news url from the website and save them into database when it's not exist
    Should be call by user when it's first time to setup::
        sudo python db_initial.py

    """
    modules = [3, 2, 1]
    urls = []
    ok_urls = [] #url of news that have been save successfully

    #db_module.cleandb()

    for module in modules:
        print " updating module", diction[module], "..."
        urls = api.get_news_urls(module)

        count = 0
        print " saving news into sysunewsDB.news...\n+------------------------------------"
        for url in urls:
            if db_module.check_news(api.get_newsid(url)):
                continue
            count = count + 1
            try:
                news = api.get_news(url)

                if len(news):
                    db_module.save_news(news)
                    ok_urls.append(url)  # actually not used, save when save news!

            except urllib2.HTTPError:
                print " failed to saving news " + str(count) + ": " + news["h1"]
                pass # Handle error here.
        print "+------------------------------------\n Finished", count, "new news found!\n"


def update():
    """update the database

    This function will be use in server.py to check whether there is new news post into the website every 10 minutes and save new news into database,

    """
    for module in [1, 2, 3]:
        key = False # new news found or not
        print "updating module,", diction[module], 
        newsids = api.get_newsid_firstpage(module)

        for newsid in newsids:
            url = 'http://news2.sysu.edu.cn/news0' + str(module) + '/' + str(newsid) + '.htm'
            if not db_module.check_news(newsid):
                print "\nnew news found: ", newsid,
                db_module.save_news(api.get_news(url))
                db_module.save_urls([url])
                print "saving  into database...",
                key = True

        if not key:
            print "no new post found!"
