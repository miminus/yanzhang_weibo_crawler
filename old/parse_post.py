#coding=utf-8
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from sgmllib import SGMLParser
import re,chardet,sys
reload(sys)
sys.setdefaultencoding('utf8')


f=open(r'C:\Users\MINUS\Desktop\work\Ziqi\posts.txt','rb')
post_content=f.read()
f.close()
print chardet.detect(post_content)
post_content=post_content.decode('gb2312').encode('utf-8')


post_con_pattern=re.compile(r'(<div class=\"WB_feed_type.*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>)',re.S)

post_con=re.findall(post_con_pattern,post_content)
if len(post_con)==0:
	sys.exit(0)

cnt=0
listname=ListName()
listname.feed(post_content)
for item in listname.name:
	print item
	cnt+=1
	print '+++++++++++++++++++++++++++++++++'
listname.close()

print cnt

