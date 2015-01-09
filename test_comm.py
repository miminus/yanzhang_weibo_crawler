#coding=utf-8
import time
import sys
import MySQLdb as mdb
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
import setting
import pickle

##################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()

##################################################


blocks_pattern=re.compile(r'list_li.*?</div>\s*</div>\s*</div>\s*</div>',re.S)
commention_pattern=re.compile(r'(<div class="wb_text".*?)<div class="wb_func',re.S)
commenterid_pattern=re.compile(r'usercard="id=(\d+)"',re.S)
commenter_pattern=re.compile(r'nick=(.*?)&amp')
time_pattern=re.compile(r'<div class="wb_from s_txt2.*?</div>')
commentid_pattern=re.compile(r'comment_id="(\d+)"')
sub_p=re.compile('<[^<>]*?>|\r',re.S)
expression_pa=re.compile(r'<img title="(.*?)".*?>',re.S)
#url='http://weibo.com/aj/v6/comment/big?_wv=5&ajwvr=6&id=3778378664454250&max_id=3778581241309347&page=5'
#url='http://weibo.com/aj/v6/mblog/info/big?_wv=5&ajwvr=6&id=3778575570253180'
##########################################################
def pythonReSubDemo(s):
    """
        demo Pyton re.sub
    """
    ss=s
    def _add111(matched):
        intStr = matched.group(); #123
        expre=re.findall(expression_pa,intStr)[0]
        return expre
    ex=re.findall(expression_pa,ss)
    
    replacedStr = re.sub(expression_pa, _add111, ss, len(ex));
    return replacedStr
#########################################################

mid=sys.argv[1]
#mid='3778378664454250'
comm_page=int(sys.argv[2])
#comm_page=2
ori_poster=sys.argv[3]
ori_postid=sys.argv[4]
user_lists=[]

driver=webdriver.Ie()
driver.get('http://weibo.com')
time.sleep(3)
#comm_page=2
for page in range(comm_page):
    url='http://weibo.com/aj/v6/comment/big?_wv=5&ajwvr=6&id='+mid+'&page='+str(page+1)
    driver.get(url)
    time.sleep(3)

    con=driver.page_source.lower()
    con=main_get(con)
    # f=open('d:/123.txt','wb')
    # f.write(con)
    # f.close()

    blocks=re.findall(blocks_pattern,con)
    print len(blocks)

    for b in blocks:
        scratch_time = time.strftime('%Y-%m-%d %H:%M:%S')
        ##################################################
        comment_id=re.findall(commentid_pattern,b)[0]
        #print comment_id
        ##################################################
        commenter=re.findall(commenter_pattern,b)[0]
        #print commenter
        
        
        ##################################################
        commenter_id=re.findall(commenterid_pattern,b)[0]
        user_lists.append(commenter_id)
        #print commenter_id
        ##################################################
        
        commention=re.findall(commention_pattern,b)[0]
        commention=pythonReSubDemo(commention)
        commention=re.sub(sub_p,'',commention)
        commention_con=commention.replace('\n','')
        # print commention_con
        commention=commention_con.encode('gbk','ignore')
        #print chardet.detect(commention)
        
        ##################################################
        cc='回复@(.*?):'
        #print chardet.detect(cc)
        reply_pa=re.compile(cc)
        flag=0
        try:
            reply_to=re.findall(reply_pa,commention)[0]
            print reply_to+'  _____________________________'
            reply_to=reply_to.decode('gbk').encode('utf-8')
            flag=1
        except:
            pass
        if flag==1:
            fm="comment"
            query1="insert ignore into reply_to(ori_postid,pp_id,poster_id,poster,postee,fm) values(%s,%s,%s,%s,%s,%s)"
            param1=(mid,comment_id,commenter_id,commenter,reply_to,fm)
            cur.execute(query1,param1)
            db.commit()
        ##################################################
        time_con=re.findall(time_pattern,b)[0]
        time_con=time_con.decode('utf-8','ignore').encode('gbk','ignore')
        #print chardet.detect(str(time))
        post_time=''
        if '今天' in time_con:
            a_pa=re.compile('\d{2}:\d{2}')
            timer=re.findall(a_pa,time_con)[0]
            date=str(time.strftime('%Y-%m-%d'))
            post_time=date+' '+timer+':00'
           
        elif '月' in time_con and '日' in time_con:
            b_pa=re.compile('(\d+)月(\d+)日 (\d+:\d+)')
            timer=re.findall(b_pa,time_con)[0]
            year=str(time.localtime().tm_year)
            date=year+'-'+timer[0]+'-'+timer[1]+' '+timer[2]+':00'
            post_time = date
        
        #print post_time
        query="insert ignore into post (post_id,poster,poster_id,content,scratch_time,post_time) values(%s,%s,%s,%s,%s,%s)"
        params=(comment_id,commenter,commenter_id,commention_con,scratch_time,post_time)
        cur.execute(query,params)		
        db.commit()
        ori_poster='微博赛事'
        #ori_poster=ori_poster.encode('utf-8')
        #print chardet.detect(ori_poster)
        fm='comment'
        query="insert ignore into replyto (comm_id,commer,commer_id,ori_post_id,ori_poster,ori_poster_id,fm) values(%s,%s,%s,%s,%s,%s,%s)"
        param=(comment_id,commenter,commenter_id,mid,ori_poster,ori_postid,fm)
        cur.execute(query,param)
        db.commit()
        ##################################################
        
        print '+_+'
    time.sleep(0)
    
driver.quit()

with open('%s/comm_userlists.txt' %(setting.CURRENT_PATH),'wb') as f:
    pickle.dump(user_lists,f)
os.system('python %s/test_comm_userlists.py' % (setting.CURRENT_PATH))



'''
for user in user_lists:
    main_usr_url='http://weibo.com/'+user
    query1='select user_id from weibo_user'
    cur.execute(query1)
    res=cur.fetchall()
    flag_cf=0
    for i in res:
        ress=i[0]
        if user == str(ress):
            flag_cf=1
    if flag_cf==1:
        continue
    os.system('python %s/user_homepage.py %s' % (setting.CURRENT_PATH,main_usr_url))
sys.exit(0) 
'''