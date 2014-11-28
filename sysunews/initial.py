"""initialize the database

When it's the first time to deploy this server program, please enter directory sysunews/,
and run this follow two commands

    mysql -u root -p
    source db_initial.sql

after this two commands, a database sysunewsDB with two table (urls & news) will have been created in your mysql, and then execute

    python initial.py

This will crawl news from news.sysu.edu.cn and save them into the database created before

"""
import urllib2
import cookielib
import time
import sysunews.api as api
import sysunews.db_update as db_update

db_update.initial()
