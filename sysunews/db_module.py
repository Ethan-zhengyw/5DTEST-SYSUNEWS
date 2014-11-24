import os
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

    return result


def check_news(newsid):

    sql = 'select * from urls where newsid=' + str(newsid)
    cursor.execute(sql)
    for item in cursor.fetchall():
        for attr in item:
            if str(newsid) == str(attr):
                return True

    return False


def get_module_newsNum(module):
    sql = 'select count(newsid) from urls where module=' + str(module)
    cursor.execute(sql)
    for item in cursor.fetchall():
        for attr in item:
            return attr

    return 0
