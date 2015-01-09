#coding=utf-8
import re
import chardet
def tranun(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\' and s[i+1]=='u':
			ss=ss+unichr(int(s[i+2:i+6],16))
			i=i+6
		else:
			ss=ss+s[i]
			i=i+1
	return ss
def tran(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\':
			i=i+1
		else:
			ss=ss+s[i]
			i=i+1
	return ss

def main(path):
	Path='d:/'+path
	f=open(Path,'rb')
	a=f.read()
	print a
	print chardet.detect(str(a))
	a=a.decode('ascii').encode('utf-8')
	print chardet.detect(str(a))
	#print a
	b=tranun(a)
	#c=tran(b)
	print chardet.detect(str(b))
	print b
	#pattern=re.compile(r'rnt{0,25}|t{3,25}',re.S)
	#d=re.sub(pattern,'',c)
	'''
	print d
	f.close()
	f=open('d:/hehe.txt','wb')
	f.write(d)
	f.close()
	'''
def main_get(content):
	content=tranun(content)
	content=tran(content)
	content=content.replace('>n','>')
	#pattern=re.compile(r'rnt{0,25}|t{2,25}',re.S)
	content=content.replace('&lt;','<')
	content=content.replace('&gt;','>')
	content=content.replace('\'','')
	content=content.replace('>n','>')    
	#content=re.sub(pattern,'',content)
	return content
if __name__=='__main__':
	main('weibo1.txt')
