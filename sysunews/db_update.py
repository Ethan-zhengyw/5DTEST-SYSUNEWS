#-*-encoding: utf-8-*-
import urllib2
import api
import db_module
import errno


def initial():
    modules = [2, 3, 1]
    urls = []

    #db_module.cleandb()

    for module in modules:
        print " updating module", module, "..."
        urls = api.get_news_urls(module)
###################################################################################################
        #if module != 1: ########
        #db_module.save_urls(urls)

        count = 0
        #key = False;    ###########
        print " saving news into sysunewsDB.news...\n+------------------------------------"
        for url in urls:
            count = count + 1
            #if key:                                                       ######
            try:
                news = api.get_news(url)
                if len(news):
                    db_module.save_news(news)

            except urllib2.HTTPError:
                print " failed to saving news " + str(count) + ": " + news["h1"]
                pass # Handle error here.
            #if url == 'http://news2.sysu.edu.cn/news01/116503.htm':  #####
            #    key = True                                         ####
        print "+------------------------------------\n Finished", count, "new news found!\n"
######################################################################################################
#       第一次使用的时候首先要调用本函数把数据存储到本地
#       运行本函数的过程中可能会有错误,解决方法如下
#           两行注释之间的注释取消,调整缩进,并将if url == '': 中地值改为终端中最后一条记录saving .... 的url值


def update():
    for module in [1, 2, 3]:
        newsids = api.get_newsid_firstpage(module)

        for newsid in newsids:
            url = 'http://news2.sysu.edu.cn/news0' + str(module) + '/' + str(newsid) + '.htm'
            db_module.save_news(api.get_news(url))
