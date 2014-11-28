#-*-encoding: utf-8-*-
"""Main Request object

This file contains some definition of Request object to be used in api to get the content of certain website page

"""
import urllib2

# Request header
header = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3; .NET4.0E; Shuame)"
}

def req_get_news_urls(module, index=""):
    """get a request object

    Args:
        module (int): 1  - 中大新闻 2  - 每周聚焦 3  - 媒体中大
        index (str): certain page of a module

    Returns:
        Request: a Request object

    """
    module_url = 'http://news2.sysu.edu.cn/news0' + str(module) + '/index' + str(index) + '.htm'
    req = urllib2.Request(
        url = module_url,
        headers = header
    )

    return req


def req_easy_req(address):
    """get a simple request object 

    Args:
        address (str): the url to open

    Returns:
        Request: a Request object

    """
    req = urllib2.Request(
        url = address,
        headers = header
    )
    return req


def req_get_news(news_url):
    """get a Request object

    Args:
        news_url (str): an url of a news like: [http://news2.sysu.edu.cn/news01/141185.htm]

    Returns:
        Request: a Request object to open a news url
    """
    return req_easy_req(news_url)
