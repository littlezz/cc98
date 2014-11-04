import httplib2 as ht2

from urllib.parse import *
import urllib.parse
from bs4 import BeautifulSoup as bs
import hashlib
import random,os


print(os.getcwd())
rpbase="http://www.cc98.org/SaveReAnnounce.asp?"
with open("./data/resp.txt",encoding="utf-8") as f:
    contents=[]
    for i in f:
        contents.append(i.rstrip())


def login(username,passwd,url,head):
    
    passwd=hashlib.md5(passwd.encode()).hexdigest()
    
    PostForm=(('a','i'),('u',username),('p',passwd),('userhidden','2'))
    PostForm=urlencode(PostForm)
    
    h=ht2.Http('.cache')
    req,u=h.request(url,"POST",headers=head,body=PostForm)
    headcp=head.copy()
    s=headcp['Cookie']=req['set-cookie']
    pd=s.split("password=")[1].split(";")[0]
    print('ok')
    headcp.pop('X-Requested-With')
    return headcp,pd

def req(url,head):
   
    res,u=h.request(url,headers=head)
    print(url)
    u=bs(u)
    fu=u.find(attrs={"name":"followup"}).get("value")
    BdidRtid=urllib.parse.parse_qsl(urlparse(url).query)
    mt=('method','fastreply')
    bdid=('BoardID',BdidRtid[0][1])
    dt=(mt,bdid)
    reurl=rpbase+urlencode(dt)
    print(reurl)
    return reurl,BdidRtid[1][1],fu

def reply(head,url,pd,rtid,fu,username):
    fu=('followup',str(fu))
    rtid=('RootID',rtid)
    star=('star','1')
    user_name=('UserName',username)
    pswd=('passwd',pd)
    ep=("Expression","face7.gif")
    content=("Content",random.choice(contents))
    
    sn=("signflag","yes")
    contentForm=(fu,rtid,star,user_name,pswd,ep,content,sn)
    
    print(urlencode(contentForm))
    print(random.choice(contents))
    h=ht2.Http('.cache')
    req,u=h.request(url,"POST",headers=head,body=urlencode(contentForm))
    
    
    
    
"""    
#
ht2.debuglevel=1
with open('head.pickle','rb')as f:
    head=pickle.load(f)
#
"""
h=ht2.Http('.cache')

    

    
    
