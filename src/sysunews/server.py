#-*- coding: utf-8 -*-
"""server module

This module help to run a server program to solve HTTP get request from client base on webpy framwork

"""
import web
import json
import thread
import time
import os
import os.path

import api
import db_update
import db_module

# urls mapping
urls = (
    '/news', 'Getnews',
    '/newshtml', 'Getnews_html',
    '/able', 'GetnewsNum',
    '(/home/images/.*)', 'Images'
)

app = web.application(urls, globals())
hostIP = os.popen('ifconfig | grep inet | grep -v inet6 | grep -v 127 | cut -d ":" -f 2 | cut -d " " -f 1').read()[:-1]

class GetnewsNum:
    """Class to solve url /able

    Request url must contains a parameter
        /able?module=1

    """
    def GET(self):
        """get the num of news is certain module

        :returns: (json) `key` - count & `value` - the number of news of certain module in database::

        """
        web.header("Content-Type","application/json; charset=utf-8")
        data = web.input(module="module")
        module = data["module"]
        count = db_module.get_module_newsNum(module)
        result = json.dumps({"count": count})
        return result

class Getnews:
    """Class to solve url /news
    
    Can solve url with three parameters
        /news?module=1&start=1&num=1

    """
    def GET(self):
        """Get news as json object

        :returns: `newslist` - a list of news in json type

        """
        web.header("Content-Type","application/json; charset=utf-8")

        data = web.input(module="module", start="start", num="num", type="type")
        module = data["module"]
        start = data["start"]
        num = data["num"]
        type_ = data["type"]

        module = (1 if module == "module" else module)
        start = (1 if start == "start" else start)
        num = (1 if num == "num" else num)

        news = api.get_news_fromDB(int(module), int(start), int(num))

        if type_ != "html":
            return json.dumps(news)
        else:
            web.header("Content-Type","text/html; charset=utf-8")
            html = ""
            for item in news:
                html = html + item["maindiv"]
            return html



class Getnews_html:
    """Class to solve url /news
    
    Can solve url with three parameters::
        /news?module=1&start=1&num=1

    """
    def GET(self):
        """get html content of news
        
        :returns: `htmltext` - html contents of news that being request, can display in a pretty way in browser

        """
        web.header("Content-Type","text/html; charset=utf-8")

        data = web.input(module="module", start="start", num="num")
        module = data["module"]
        start = data["start"]
        num = data["num"]

        module = (1 if module == "module" else module)
        start = (1 if start == "start" else start)
        num = (1 if num == "num" else num)

        news = api.get_news_fromDB(int(module), int(start), int(num))

        #return news[0]["maindiv"]
        html = ""
        for item in news:
            html = html + item["maindiv"]
        return html


class Images:
    """Handler that solve url /home/images/*
    """

    def GET(self, url):
        """Get a images with a url

        the url is the path to a images that has been saved in local directory /home/images/

        :param url: image url like [/home/images/content/...]

        """
        try:
            f = open(url, 'r')
            image = f.read()
            f.close()
        except:

            db_module.resave_img(url[5:])

            f = open(url, 'r')
            image = f.read()
            f.close()

        return image


# update news every x minutes
def update_news_intime(minutes):
    """update the news database
    
    :param minutes: update the database every 10 minutes when minutes = 10

    """
    while True:
        db_update.update()
        time.sleep(60 * minutes)

if __name__ == '__main__':
    thread.start_new_thread(update_news_intime, (10,)) # start a thread to update the database every 10 minutes
    app.run() # start the web server
