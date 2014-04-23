#!python3


"""
passwd==password
pd==passwd (in Cookie)

no cookie record Ver
"""

import Lib.logrp as logrp
import pickle
import os
os.chdir('data')

with open('username.txt',encoding="utf-8") as f:
    usernames=[]
    for i in f:
        usernames.append(i.rstrip())

with open('password.txt',encoding="utf-8") as f:
    passwds=[]
    for i in f:
        passwds.append(i.rstrip())

with open('head.pickle','rb')as f:
    loghead=pickle.load(f)


url=input('enter the url\n')
rpNum=int(input("用多少个马甲\n"))
rpNum=min(rpNum,len(passwds))
logurl='http://www.cc98.org/sign.asp'

for i in range(rpNum):
    username=usernames[i]
    passwd=passwds[i]

    head,pd=logrp.login(username,passwd,logurl,loghead)
    head["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    head["Content-Type"]="application/x-www-form-urlencoded"
    
    reurl,rtid,fu=logrp.req(url,head)
    logrp.reply(head,reurl,pd,rtid,fu,username)
    print('over')

    


