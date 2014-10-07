#-*-encoding: utf-8-*-
import web
import json
import api

# http://localhost:1234/news?module=2&start=504&num=1
urls = (
    '/news', 'Getnews',
    '/newshtml', 'Getnews_html',
    '(/home/images/.*)', 'Images'
)

app = web.application(urls, globals())

class Getnews:

    def GET(self):
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

    def GET(self):
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

    def GET(self, url):
        try:
            print url
            f = open(url, 'r')
            image = f.read()
            f.close()
            return image
        except:
            return '' # you can send an 404 error here if you want

if __name__ == "__main__":
    app.run()
