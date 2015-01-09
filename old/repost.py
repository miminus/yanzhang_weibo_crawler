#coding=utf-8
import time
import sys
import os,chardet
from selenium import webdriver
import urllib2,re
from unicode_normal import main_get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
#罗昌平 投资界 MOOC
print 'start'
reload(sys) 
sys.setdefaultencoding('utf8')
post_id=sys.argv[1]
comm_page=int(sys.argv[2])

#url='http://weibo.com/aj/comment/big?_wv=5&id=3683095809935767&page=1'

image_url_pattern=re.compile(r'src=\"(.*?)\"',re.S)
id_pattern=re.compile(r'\/(\d+)\/',re.S)
poster_pattern=re.compile(r'alt=\"(.*?)\"',re.S)
#driver=webdriver.PhantomJS()
driver=webdriver.Ie()
#driver=webdriver.Ie(executable_path='C:\Users\MINUS\AppData\Local\Google\Chrome\Application\IEDriverServer.exe')
print 'go in'
#driver.get("http://www.weibo.com")
base_url='http://weibo.com/aj/comment/big?_wv=5&id=3716227136365799&page=3'
#driver.get('http://weibo.com/1364882532/B6fHNlmh8?type=repost')
#driver.get('http://weibo.com/aj/comment/big?_wv=5&id=3716227136365799&page=3')
for page in range(comm_page):
	url='http://weibo.com/aj/comment/big?_wv=5&id='+post_id+'&page='+str(page+1)
	#print url
	driver.get(url)
	print driver.title
	print driver.current_url  #获取当前网页url
	print driver.name
	f=open(r'C:\Users\MINUS\Desktop\work\weibo_reaseach\page.txt','wb')
	time.sleep(5)
	con=driver.page_source
	con=con.lower()
	#print con
	con=main_get(con)
	f.write(con)
	f.close()
	os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\parse_comm.py')
	#########################################################################################
	time.sleep(2)
driver.quit()