#coding=utf-8
import time
import sys
import os,chardet
from selenium import webdriver
import urllib2,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from keys_to_url import geturl
print 'start'

current_dir=os.path.dirname(sys.argv[0]).replace('\\','/')
#current_file=os.path.



reload(sys) 
sys.setdefaultencoding('utf8')

image_url_pattern=re.compile(r'src=\"(.*?)\"',re.S)
id_pattern=re.compile(r'\/(\d+)\/',re.S)
poster_pattern=re.compile(r'alt=\"{0,1}(.*?)\"{0,1} src',re.S)

post_url_quote=geturl()   #获取url编码
baseurl='http://s.weibo.com/wb/'+post_url_quote+'&xsort=time&page='
page=1
#driver=webdriver.PhantomJS()
while page<=50:
	f=open(r'C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\posts.txt','wb')
	while True:
		try:
			driver=webdriver.Ie()
			url=baseurl+str(page)
			print 'go in'
			print url
			page=page+1
			driver.get("http://s.weibo.com")
			#driver.get('http://weibo.com/p/1035051189591617/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=3#feedtop')
			print driver.title
			print driver.current_url 
			print driver.name

			time.sleep(5)
			driver.get(url)
			element = WebDriverWait(driver,12).until(EC.presence_of_element_located((By.ID,"weibo_top_public")))
			lists_map=driver.find_elements_by_xpath('//dl[@mid]')
			
			break
			
			
		except:
			continue
			driver.quit()
	#driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","") 
	#time.sleep(5)
	#driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","") 
	#time.sleep(5
	cnt=0
	#################################################################################
	
	for i in lists_map:
		content=i.get_attribute('outerHTML')
		content=content.decode('utf-8','ignore')
		soup=BeautifulSoup(content)
		f.write(soup.prettify())
		f.write('\r\n')
		print chardet.detect(content)
		cnt=cnt+1
		#print content
	print cnt
	f.close()
	time.sleep(5)
	driver.quit()
	os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\parse_sina.py')
'''


time.sleep(20)

#driver.quit()
#driver.page_source  获取全页代码
'''
'''
time.sleep(2)
list=driver.find_elements_by_class_name('info_list')
username=driver.find_element_by_name('username')
#driver.execute_script("$('input.W_input.W_input_focus').attr('style','opacity:1;display:block;')")
#username = driver.find_element_by_css_selector('input.W_input.W_input_focus') 
passwd=driver.find_element_by_name('password')
#submit=driver.find_element_by_class_name('login_btn')
submit=driver.find_element_by_css_selector('.info_list.login_btn')
print 'ok'
print username
print passwd
print submit

#elem=WebDriverWait().until(username.is_displayed())
#elem_visible = WebDriverWait(driver,29).until(lambda the_driver : the_driver.find_element_by_name('username').is_displayed())
# username.is_displayed())

#inputs = driver.execute_script("var labels = arguments[0], inputs = []; for (var i=0; i < labels.length; i++){" #"inputs.push(document.getElementById(labels[i].checked=true)); } return inputs;",username)
driver.execute_script("arguments[0].style.display='block';",username)

print username.is_displayed()
print passwd.is_displayed()
print submit.is_displayed()

list[0].click()
time.sleep(1)
list[0].send_keys('m189111@163.com')
list[1].click()
time.sleep(1)
list[1].send_keys('********')
print '1'
submit.submit()
print 'ok put'
'''
