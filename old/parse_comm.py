#coding=utf-8
import re,sys
import MySQLdb as mdb
import time

#################################################
db = mdb.connect(host="localhost",user="root",passwd="minus",db="public_opinion",charset="utf8" )
cur=db.cursor()
###############################################

f=open(r'C:\Users\MINUS\Desktop\work\weibo_reaseach\page.txt','rb')
page_content=f.read()
f.close()

content_pattern=re.compile(r'(<dl.*?<\/dl>)',re.S)
post_id_pattern=re.compile(r'mid=(\d+)',re.S)
comm_id_pattern=re.compile(r'cid=(\d+)',re.S)
commenter_pattern=re.compile(r'title=.{0,1}\"(.*?)\"',re.S)
commenter_homepage_pattern=re.compile(r'href=.{0,1}\"(.*?)\"',re.S)
commenter_id_pattern=re.compile(r'id=(\d+)',re.S)
commention_pattern=re.compile(r'<dd.*?>.*?(<a.*?)<span class',re.S)
commter_image_pattern=re.compile(r'<img.*?src=.{0,1}\"(.*?)\"',re.S)

sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
def parse_html_content(str):
    '''return a unicode string'''
    str = re.sub(sub_p_1, '', str)    
    str = str.replace('&nbsp;', ' ')
    str = str.replace('&amp;', '')
    str = str.replace('#039;', '')
    str = str.replace('#', '')
    str = str.replace('&#160;', ' ')
    str = str.replace('&lt;', '<')
    str = str.replace('&gt;', '>')
    str = str.replace('&amp;', '&')
    str = str.replace('&quot;', '"')
    ustr = str
    return ustr

content=re.findall(content_pattern,page_content)
print len(content)
for i,d in enumerate(content):
	scratch_time=time.strftime('%Y-%m-%d %H:%M:%S')
	print scratch_time
	#########################################
	comm_id=re.findall(comm_id_pattern,d)[0]
	#print comm_id
	##########################################
	post_id=re.findall(post_id_pattern,d)[0]
	#print post_id
	#########################################
	commenter_image=re.findall(commter_image_pattern,d)[0]
	#print commenter_image
	#########################################
	commenter=re.findall(commenter_pattern,d)[0]
	#commenter=commenter.replace('\'','')

	#print commenter.decode('utf-8').encode('gbk')
	#########################################
	commenter_homepage=re.findall(commenter_homepage_pattern,d)[0]
	commenter_homepage='http://www.weibo.com'+commenter_homepage
	#print commenter_homepage
	########################################
	commenter_id=re.findall(commenter_id_pattern,d)[0]
	#print commenter_id
	########################################
	commention=re.findall(commention_pattern,d)
	commention=map(lambda x:parse_html_content(x),commention)[0]
	#print commention
	##########################################
	
	query='insert ignore into comment (comment_id,commenter_id,commenter,commenter_image,comment_content,post_id,scratch_time) values(%s,%s,%s,%s,%s,%s,%s)'
	params=(comm_id,commenter_id,commenter,commenter_image,commention,post_id,scratch_time)
	
	cur.execute(query,params)
	db.commit()
	
	print '+++++++++++++++++++++++++'
cur.close()