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


def save_urls(urls):

    print " saving urls into sysunewsDB.urls...\n+------------------------------------"
    count = 0
    length = len(urls)

    for url in urls:
        count = count + 1

        newsid = api.get_newsid(url)
        module = api.get_module(url)
        param = [newsid, module, url]

        print " saving url " + str(count) + "/" + str(length) + ": " + url
        cursor.execute('insert into urls values(%s, %s, %s)', param)

    con.commit()
    print "+------------------------------------\n Finished ", count, "new url fetched!\n"


def save_news(news):

    print " saving news: " + news["url"] + " " + news["h1"]
    pattern = '('
    pattern_sql = '('
    param = []

    for attr in news:
        attr_str = str(news[attr])
        if attr == "imgs" and len(news["imgs"]) != 0:
            for img_url in news["imgs"]:
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
    con.commit()


def save_img(url):
    dirname = '/home/' + url[:url.rfind('/')]
    filename = '/home/' + url

    if not os.path.isfile(filename):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        image = open(filename, 'wb')
        image.write(urllib.urlopen('http://news2.sysu.edu.cn/' + url).read())
        image.close()


def check_news(tablename, newsid):

    cursor.execute('select newsid from ' + tablename + ' where newsid = %s', newsid)
    result = cursor.fetchone()

    return (True if result else False)


def cleandb():

    cursor.execute('truncate table urls')
    cursor.execute('truncate table news')
    con.commit()


def get_news(module, start, num):

    patterns = ["newsid", "module", "visit_times", "date", "url", "imgs", "author", "editor", "h1", "h2", "source", "maindiv"]
    result = []

    sql = 'select * from news where module=' + str(module)

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

    return result
