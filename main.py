#coding=utf-8
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import time,math
import MySQLdb as mdb
import re,chardet,sys
import os,setting
import subprocess
reload(sys)
sys.setdefaultencoding('utf8')
#######################################


#################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()
###############################################
post_id=setting.POST_ID
user_id=setting.USER_ID
main_poster=setting.MAIN_POSTER


comm_page=setting.COMM_PAGE
repost_page=setting.REPOST_PAGE


c1 = subprocess.Popen('python %s/test_comm.py %s %d %s %s' %(setting.CURRENT_PATH,post_id,comm_page,main_poster,user_id))
c2 = subprocess.Popen('python %s/test_repost.py %s %d %s %s' %(setting.CURRENT_PATH,post_id ,repost_page,main_poster,user_id))
c1.wait()
c2.wait()