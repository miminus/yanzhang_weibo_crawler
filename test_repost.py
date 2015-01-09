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
import MySQLdb as mdb
import setting
import pickle
##################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()

##################################################
expression_pa=re.compile(r'<img title="(.*?)".*?>',re.S)
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
###########################################    
#url='http://weibo.com/aj/v6/comment/big?_wv=5&ajwvr=6&id=3778378664454250&max_id=3778581241309347&page=5'
#url='http://weibo.com/aj/v6/mblog/info/big?_wv=5&ajwvr=6&id=3778575570253180'

mid=sys.argv[1]
#mid='3778378664454250'
repost_page=int(sys.argv[2])
ori_poster=sys.argv[3]
ori_postid=sys.argv[4]
#repost_page=2
#url='http://weibo.com/aj/v6/mblog/info/big?_wv=5&ajwvr=6&id=3775834063880888&max_id=3778505924091530&page=5&__rnd=1416385881949'
driver=webdriver.Ie()
driver.get('http://www.weibo.com')
time.sleep(3)
user_lists=[]
for page in range(repost_page):
    url='http://weibo.com/aj/v6/mblog/info/big?_wv=5&ajwvr=6&id='+mid+'&page='+str(page+1)
    driver.get(url)
    con=driver.page_source.lower()
    con=main_get(con)
    # f=open('d:/123.txt','wb')
    # f.write(con)
    # f.close()

    blocks_pattern=re.compile(r'class="list_li.*?</div>\s*</div>\s*</div>\s*</div>',re.S)
    repostid_pattern=re.compile(r'mid="(\d+)"')
    reposter_pattern=re.compile(r'img alt="(.*?)"')
    reposterid_pattern=re.compile(r'usercard="id=(\d+)"')
    content_pattern=re.compile(r'(<div class="wb_text".*?)<div class="wb_func',re.S)
    date_pattern=re.compile(r'date="(\d{13})"')
    sub_p=re.compile('<[^<>]*?>|\r',re.S)


    blocks=re.findall(blocks_pattern,con)
    print len(blocks)


    for b in blocks:
        scratch_time = time.strftime('%Y-%m-%d %H:%M:%S')
        ##################################################
        repost_id=re.findall(repostid_pattern,b)[0]
        #print repost_id
        
        ##################################################
        reposter=re.findall(reposter_pattern,b)[0]
        #print reposter
        ##################################################
        reposter_id=re.findall(reposterid_pattern,b)[0]
        #print reposter_id
        user_lists.append(reposter_id)
        
        ##################################################
        content_all=re.findall(content_pattern,b)[0]
        content_all=pythonReSubDemo(content_all)
        f=open('d:/123.txt','wb')
        f.write(content_all)
        f.close()
        content=re.sub(sub_p,'',content_all)
        content_con=content.replace('\n','')
        # print content_con
        
        content=content_con.replace(' ','')
        content=content.encode('gbk','ignore')
        #print chardet.detect(content)  #content为gbk
        
        #content=content.decode('utf-8')
        #print chardet.detect(content)
        #conservation_pattern=re.compile(r'')
        ##################################################
        date=re.findall(date_pattern,b)[0]
        date=date[:-3]
        date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(date)))
        #print date
        #################################################
        person_lists=[]
        c_p='(.*?)：'.decode('utf-8').encode('gbk')
        pp=re.compile(c_p)
        #print chardet.detect(c_p)
        a=re.findall(pp,content)[0]
        a=a.decode('gbk').encode('utf-8')
        person_lists.append(a)
        #------------------------
        p_pa=re.compile(r'//@(.*?):')
        try:
            persons=re.findall(p_pa,content)
            for i in persons:
                i=i.decode('gbk').encode('utf-8')
                person_lists.append(i)
        except:
            pass
        if len(person_lists)!=1:
            for i,j in enumerate(person_lists):
                fm="repost"
                if i==0:    
                    # query1="insert ignore into reply_to(ori_postid,pp_id,poster_id,poster,postee,postee_id,fm) values(%s,%s,%s,%s,%s,%s)"
                    # param1=(mid,repost_id,reposter_id,reposter,setting.MAIN_POSTER,setting.USER_ID,fm)
                    # cur.execute(query1,param1)
                    # db.commit()
                    continue
                if i==1:
                    query1="insert ignore into reply_to(ori_postid,pp_id,poster_id,poster,postee,fm) values(%s,%s,%s,%s,%s,%s)"
                    param1=(mid,repost_id,reposter_id,reposter,j,fm)                
                else:
                    query1="insert ignore into reply_to(ori_postid,pp_id,poster,postee,fm) values(%s,%s,%s,%s,%s)"
                    param1=(mid,repost_id,person_lists[i-1],j,fm)
                    
                cur.execute(query1,param1)
                db.commit()
            query1="insert ignore into reply_to(ori_postid,pp_id,poster,postee,postee_id,fm) values(%s,%s,%s,%s,%s,%s)"
            param1=(mid,repost_id,person_lists[len(person_lists)-1],setting.MAIN_POSTER,setting.USER_ID,fm)
            cur.execute(query1,param1)
            db.commit()    
        
        #################################################
        print '++'
        query="insert ignore into post (post_id,poster,poster_id,content,scratch_time,post_time) values(%s,%s,%s,%s,%s,%s)"
        params=(repost_id,reposter,reposter_id,content_con,scratch_time,date)
        cur.execute(query,params)		
        db.commit()
        ori_poster='微博赛事'
        #ori_poster=ori_poster.encode('utf-8')
        fm='repost'
        query="insert ignore into replyto (comm_id,commer,commer_id,ori_post_id,ori_poster,ori_poster_id,fm) values(%s,%s,%s,%s,%s,%s,%s)"
        param=(repost_id,reposter,reposter_id,mid,ori_poster,ori_postid,fm)
        cur.execute(query,param)
        db.commit()
        
        
    time.sleep(0)
driver.quit()

with open('%s/repost_userlists.txt' %(setting.CURRENT_PATH),'wb') as f:
    pickle.dump(user_lists,f)
os.system('python %s/test_repost_userlists.py' % (setting.CURRENT_PATH))


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
    #print 'repost user'
    os.system('python %s/user_homepage.py %s' % (setting.CURRENT_PATH,main_usr_url))
sys.exit(0)
'''

    