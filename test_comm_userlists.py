#coding=utf-8
import os,sys,pickle
import setting
import MySQLdb as mdb
import copy,time


db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()


with open('%s/comm_userlists.txt' %(setting.CURRENT_PATH),'rb') as f:
    user_lists=pickle.load(f)
    
print len(user_lists)
new_user_lists=copy.deepcopy(user_lists)
for index,user in enumerate(user_lists):
    if (index+1)%20==0:
        print 'go sleep le'
        time.sleep(3600)
    main_usr_url='http://weibo.com/'+user
    query1='select user_id from weibo_user'
    cur.execute(query1)
    res=cur.fetchall()
    flag_cf=0
    for i in res:
        ress=i[0]
        if user == str(ress):
            flag_cf=1
    if flag_cf==0:
        os.system('python %s/user_homepage.py %s' % (setting.CURRENT_PATH,main_usr_url))
    new_user_lists.remove(user)
    with open('%s/comm_userlists.txt' %(setting.CURRENT_PATH),'wb') as f:
        pickle.dump(new_user_lists,f)
    print 'delete one'
    
sys.exit(0) 