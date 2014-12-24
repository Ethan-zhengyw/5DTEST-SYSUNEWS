sysunews
========

First test in 5D zone: crawl news of 3 module: 中大新闻,每周聚焦 and 媒体中大
  from http://news2.sysu.edu.cn/ then save into database
Implement api for getting new by http get method
    
  Basic function
-----------------------------------  
  You can execute command: sudo python server.py
  and then get news by http method get like:
  
          localhost:8080/news?module=1&start=1&num=3
  
  json type data will be returned:        
  
    [
      {
        "imgs": "[]",
        "author": "宣传部",
        "url": "http://news2.sysu.edu.cn/news02/122960.htm",
        "h1": "郑德涛书记出席附属三院2009年医院发展工作会议",
        "module": 2,
        "source": "附属三院",
        "date": "2009-04-20",
        "visit_times": 1068,
        "h2": "",
        "maindiv": "...",
        "newsid": 122960,
        "editor": ""
      },
      ...
    ]
          
  For more details please view [sysunews API.docx]

### How to deploy
  Database prepare:
  
      mysql -u sysunews -p sysunews
  
      source ./sysunews/db_init.sql
  
  Save news to localhost:
  
      sudo python ./initial.py
      
  Start host:
  
      sudo python ./sysunews/server.py

### Main dependence
  python
  
      - urllib, urllib2, cookiejar: deal with HTTP request
  
      - re: regular expression module to get information
  
      - webpy: enable localhost to serve information to other computers
  
  mysql
  
      - news will crawled will be saved in database
      
### Documention online
  
  http://sysunewsdevdoc.sinaapp.com/html/
