#-*-encoding: utf-8-*-
import urllib2

# Request header
header = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3; .NET4.0E; Shuame)"
}

# --------------------------------
# parameters:
#      1  - 中大新闻
#      2  - 每周聚焦
#      3  - 媒体中大
# --------------------------------
def req_get_news_urls(module, index=""):
    module_url = 'http://news2.sysu.edu.cn/news0' + str(module) + '/index' + str(index) + '.htm'
    req = urllib2.Request(
        url = module_url,
        headers = header
    )
    return req


def req_easy_req(address):
    req = urllib2.Request(
        url = address,
        headers = header
    )
    return req


def req_get_news(news_url):
    return req_easy_req(news_url)
