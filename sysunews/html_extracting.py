#-*-encoding: utf-8-*-
import urllib2
import cookielib
import re
import post_module

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

def find_index_range(data):

    regexp = '(?<=href="index)(\d+)'
    indexes = re.findall(regexp, data)

    start = indexes[0]
    end = indexes[1]

    return start, end


def find_news_urls(data, module):

    urls = []

    regexp = '(?<=</span><a href=")(\d+)'
    hrefnums = re.findall(regexp, data)

    for newid in hrefnums:
        urls.append('http://news2.sysu.edu.cn/news0' + str(module) + '/' + newid + '.htm')

    return urls


# -----------------------------
# Article Store structure
#     {
#         h1, h2, source, author, editor, date, visit_times, div,
#         url, module,
#         imgs = ["", "", "", ...],
#         videos ["", "", "", ...]
#     }
# -----------------------------
def find_news(data):
    news = {}

    # find title h1 and h2
    # --------------------------
    patterns = ["h1", "h2"]
    for pattern in patterns:
        regexp = '(?<=<' + pattern + ' align="center">).*?(?=</' + pattern + '>)'
        match = re.search(regexp, data)
        news[pattern] = match.group()


    # find source, author, editor and date
    # --------------------------
    patterns = {"source":"稿件来源", "author":"作者", "editor":"编辑", "date":"发布日期"}
    for pattern in patterns:
        regexp = patterns[pattern] + '：(.*?)\ '
        match = re.search(regexp, data)
        if match:
            news[pattern] = match.group(1)

    # find visit times
    # --------------------------
    # To get the read times of an article
    # a new request is needed
    regexp = r'阅读次数：<script src="(.*?)"'
    match = re.search(regexp, data)
    if match:
        req = post_module.req_easy_req(match.group(1))
        result = opener.open(req).read()
        news["visit_times"] = re.search(r'\d+', result).group()

    # find div - article div in html
    # --------------------------
    regexp = '(<div id="mainright">.*?)(<div class="clear"></div>)'
    match = re.search(re.compile(regexp, re.S), data).group(1)
    news["div"] = match[:-10]
    
    # find images src
    # --------------------------
    imgs = []
    regexp = r'<img .*?src="../(.*?)"'

    matches = re.findall(regexp, news["div"])
    if matches:
        for match in matches:
             imgs.append(match)

    news["imgs"] = imgs
    
    news["div"] = re.sub('<img src="\.\./', '<img src="/home/sysunews/', news["div"])

    return news


def find_module(url):

    return re.search('news0(\d+)', url).group(1)


def find_newsid(url):
    
    return re.search('(\d+)\.htm', url).group(1)
