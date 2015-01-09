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
# db = mdb.connect(host="localhost",user="root",passwd="minus",db="new_opinion",charset="utf8" )
# cur=db.cursor()


pa=re.compile(r'abp="\d+" ')


reload(sys) 
sys.setdefaultencoding('utf8')
#base_url='http://weibo.com/1883881851/fans?page='
base_url=sys.argv[1]
page_num=sys.argv[2]
#page_num=4
main_userid=sys.argv[3]
#main_userid='123123'
main_user=sys.argv[4]
#main_user='fdf '

follower_list=[]
flag=0

for i in range(int(page_num)):
	page_url=base_url+str(i+1)
	print page_url
	#f=open('C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\follower.txt','wb')
	while True:
		try:
			if flag==0:
				driver=webdriver.Ie()	
			flag=1
			#driver.implicitly_wait(10)
			print 'go in'
			driver.get(page_url)
			driver.refresh()            
			#time.sleep(2)
			element = WebDriverWait(driver,12).until(EC.presence_of_element_located((By.ID,"pl_common_top")))
			#print element
			main_area=driver.find_element_by_class_name('follow_list')
			break
		except:
			flag=0
			driver.quit()
			continue
	content=main_area.get_attribute('outerHTML')
	soup=BeautifulSoup(content)
	
	content=soup.prettify()
	# f=open('d:/aa.txt','wb')
	# f.write(content)
	# f.close()
	content=re.sub(pa,'',content)
	######################################
	items_pattern=re.compile(r'(<li action-data="uid.*?</dd>\s*</dl>\s*</li>)',re.S)
	fnick_pattern=re.compile(r'fnick=(.*?)&amp;sex=(.)',re.S)
	uid_pattern=re.compile(r'uid=(.*?)&amp;',re.S)
	list_pattern=re.compile(r'<em class="count">(.*?)</em>',re.S)
	digit_pattern=re.compile(r'(\d+)')
	sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
	
	
	items=re.findall(items_pattern,content)
	print len(items)
	for item in items:
		fnick=re.findall(fnick_pattern,item)[0]
		if fnick[1]=='m':
			gender='male'
			#print gender
			uid=re.findall(uid_pattern,item)[0]
			lists=re.findall(list_pattern,item)
			ll=[]
			for list in lists:
				list= re.sub(sub_p_1,' ',list) 
				dig=re.findall(digit_pattern,list)[0]
				ll.append(dig)
			#print ll
		elif fnick[1]=='f':
			gender='female'
			#print gender
			uid=re.findall(uid_pattern,item)[0]
			lists=re.findall(list_pattern,item)
			ll=[]
			for list in lists:
				list= re.sub(sub_p_1,' ',list) 
				dig=re.findall(digit_pattern,list)[0]
				ll.append(dig)
			#print ll
		else:
			uid=re.findall(uid_pattern,item)[0][5:]    #话题类用户
		print uid
		follower_list.append(uid)
		print '++++++++++++++++++++++++++++'
		first_or_last='first'
		query='insert ignore into follower_followee (follower,follower_id,followee,followee_id,guanzhu,fensi,post_num,gender,first_or_last) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		param=(fnick[0],uid,main_user,main_userid,ll[0],ll[1],ll[2],gender,first_or_last)
		# cur.execute(query,param)
		# db.commit()
	if (i+1)==int(page_num):
		driver.quit()
	time.sleep(2)
sys.exit(0)
# for uid in follower_list:
	# uid='http://weibo.com/'+uid
	# os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\user_homepage.py %s' % uid)
		
		
		
		
		
		