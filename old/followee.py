#coding=utf-8
import time
import sys
import MySQLdb as mdb
import os,chardet
from selenium import webdriver
import urllib2,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from keys_to_url import geturl
print 'start'

#################################################
db = mdb.connect(host="localhost",user="root",passwd="minus",db="public_opinion",charset="utf8" )
cur=db.cursor()


reload(sys) 
sys.setdefaultencoding('utf8')
#base_url='http://weibo.com/1883881851/follow?page='
base_url=sys.argv[1]
page_num=sys.argv[2]
#page_num=4
main_userid=sys.argv[3]
main_user=sys.argv[4]


flag=0

for i in range(int(page_num)):
	page_url=base_url+str(i+1)
	#f=open('C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\follower.txt','wb')
	while True:
		try:
			if flag==0:
				driver=webdriver.Ie()	
			flag=1
			#driver.implicitly_wait(10)
			print 'go in'
			driver.get(page_url)
			element = WebDriverWait(driver,12).until(EC.presence_of_element_located((By.ID,"pl_common_top")))
			#print element
			main_area=driver.find_element_by_class_name('cnfList')
			break
		except:
			flag=0
			driver.quit()
			continue
	content=main_area.get_attribute('outerHTML')
	soup=BeautifulSoup(content)
	#print 'hehe'
	#f.write(soup.prettify())
	#f.close()
	content=soup.prettify()
	######################################
	items_pattern=re.compile(r'<li.*?>.*?</li>',re.S)
	fnick_pattern=re.compile(r'fnick=(.*?)&amp;',re.S)
	uid_pattern=re.compile(r'id=(\d+)"',re.S)
	
	
	items=re.findall(items_pattern,content)
	#print len(items)
	for item in items:
		fnick=re.findall(fnick_pattern,item)[0]
		#print fnick
		uid=re.findall(uid_pattern,item)[0]
		print uid
		query='insert ignore into follower_followee (follower,follower_id,followee,followee_id) values(%s,%s,%s,%s)'
		param=(main_user,main_userid,fnick,uid)
		cur.execute(query,param)
		db.commit()
	if (i+1)==int(page_num):
		driver.quit()


		
		
		
		
		
		