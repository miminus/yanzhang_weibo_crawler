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
import math
print 'start'

#################################################
db = mdb.connect(host="localhost",user="root",passwd="minus",db="public_opinion",charset="utf8" )
cur=db.cursor()
###############################################

#homepage=argv[1]
f=open('C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\user_main.txt','wb')
#homepage=sys.argv[1]
#homepage='http://weibo.com/u/1727186255'
homepage='http://weibo.com/kaifulee'

reload(sys) 
sys.setdefaultencoding('utf8')

#time.sleep(8)
#WebDriverWait(driver, 10)..until(EC.presence_of_element_located((By.ID,'someid')))
while True:
	try:
		driver=webdriver.Ie()
		#driver.implicitly_wait(10)
		print 'go in'
		driver.get(homepage)
		element = WebDriverWait(driver,12).until(EC.presence_of_element_located((By.ID,"pl_common_top")))
		print element
		flag=0
		try:
			main_area=driver.find_element_by_class_name('WB_frame_b')
		except:
			main_area=driver.find_element_by_class_name('PRF_profile_header')
			flag=1
		break
	except:
		driver.quit()
		continue
content=main_area.get_attribute('outerHTML')
soup=BeautifulSoup(content)
if flag==0:
	f.write(soup.prettify())
	f.close()
	content=soup.prettify()
	#############解析开始#########################
	uid_pattern=re.compile('uid=(\d+)',re.S)
	user_pattern=re.compile('fnick=(.*?)"',re.S)
	user_image_pattern=re.compile('src="(http://tp\d{1}.sinaimg.cn/.*?/[01])"',re.S)
	
	area_pattern=re.compile(r'loc=infplace" title=.*?>(.*?)</a>',re.S)
	profess_pattern=re.compile(r'loc=infjob" title=.*?>(.*?)</a>',re.S)
	tag_pattern=re.compile(r'loc=inftag"><.*?>(.*?)</span>',re.S)
	class_pattern=re.compile(r'W_level_num l(\d+)',re.S)
	digit_pattern=re.compile(r'>\s*(\d+)\s*<',re.S)
	#aa='(\d+)\s*<.*?>\s*<.*?>\s*关注'.decode('gbk').encode('utf-8')
	#followee_pattern=re.compile(aa,re.S)
	#follower_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*粉丝',re.S)
	#postnum_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*微博',re.S)
	
	uid=re.findall(uid_pattern,content)[0]
	#print uid
	user=re.findall(user_pattern,content)[0]
	#print user
	user_image=re.findall(user_image_pattern,content)[0]
	#print user_image
	try:
		area=re.findall(area_pattern,content)[0]
	except:	
		area=''
	#print area
	try:
		profess=re.findall(profess_pattern,content)[0]
	except:	
		profess=''
	print profess
	try:
		tag=''
		tags=re.findall(tag_pattern,content)
		for i in tags:
			tag=tag+i+', '
	except:	
		pass
	#print tag
	#print chardet.detect(content)
	strongs=soup.find_all('strong')
	dig=[]
	for i in strongs:
		try:
			a=re.findall(digit_pattern,str(i))[0]
			print a
			dig.append(a)
		except:
			pass
	followee_num=dig[0]
	follower_num=dig[1]
	posts_num=dig[2]
	
	if 'W_ico12 male' in content:
		gender='male'
	elif 'W_ico12 female' in content:
		gender='female'
	else:
		gender=''
	#print gender
	_class=re.findall(class_pattern,content)[0]
	#print _class
	

	
if flag==1:
	content=soup.find_all("div",class_="profile_top S_bg5")
	content = content[0]
	#f.write(content.prettify())
	#f.close()
	content=str(content)
	#############解析开始#########################
	uid_pattern=re.compile('uid=(\d+)',re.S)
	user_pattern=re.compile('fnick=(.*?)"',re.S)
	user_image_pattern=re.compile('src="(http://tp\d{1}.sinaimg.cn/.*?/\d{1})"',re.S)
	area_pattern=re.compile(r'loc=infplace" title=.*?>(.*?)</a>',re.S)
	profess_pattern=re.compile(r'loc=infjob" title=.*?>(.*?)</a>',re.S)
	tag_pattern=re.compile(r'loc=inftag"><.*?>(.*?)</span>',re.S)
	class_pattern=re.compile(r'W_level_num l(\d+)',re.S)
	digit_pattern=re.compile(r'>\s*(\d+)\s*<',re.S)
	#aa='(\d+)\s*<.*?>\s*<.*?>\s*关注'.decode('gbk').encode('utf-8')
	#followee_pattern=re.compile(aa,re.S)
	#follower_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*粉丝',re.S)
	#postnum_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*微博',re.S)
	
	uid=re.findall(uid_pattern,content)[0]
	#print uid
	user=re.findall(user_pattern,content)[0]
	#print user
	try:
		user_image=re.findall(user_image_pattern,content)[0]
	except:
		sys.exit()
	#print user_image
	try:
		area=re.findall(area_pattern,content)[0]
	except:	
		area=''
	print area
	try:
		profess=re.findall(profess_pattern,content)[0]
	except:	
		profess=''
	print profess
	try:
		tag=''
		tags=re.findall(tag_pattern,content)
		for i in tags:
			tag=tag+i+', '
	except:	
		pass
	#print tag
	#print chardet.detect(content)
	strongs=soup.find_all('strong')
	dig=[]
	for i in strongs:
		try:
			a=re.findall(digit_pattern,str(i))[0]
			print a
			dig.append(a)
		except:
			pass
	followee_num=dig[0]
	follower_num=dig[1]
	posts_num=dig[2]
	
	if 'W_ico12 male' in content:
		gender='male'
	elif 'W_ico12 female' in content:
		gender='female'
	else:
		gender=''
	#print gender
	_class=re.findall(class_pattern,content)[0]
	#print _class
			
			
query='insert ignore into weibo_user (user_id,user_name,user_image,gender,area,profession,tags,class,post_num,follower_num,followee_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
params=(uid,user,user_image,gender,area,profess,tag,_class,posts_num,follower_num,followee_num)			
cur.execute(query,params)
db.commit()
driver.quit()
#####################访问关注与粉丝#############################
follower_url='http://weibo.com/'+uid+'/fans?page='
followee_url='http://weibo.com/'+uid+'/follow?page='

follower_page=int(math.ceil(float(int(follower_num)/20.0)))
followee_page=int(math.ceil(float(int(followee_num)/20.0)))
if follower_page>10:
	follower_page=10
if followee_page>10:
	followee_page=10
	
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\follower.py %s %d %s %s' %(follower_url,follower_page,uid,user))
time.sleep(4)
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\followee.py %s %d %s %s' %(followee_url,followee_page,uid,user))


###################################################















