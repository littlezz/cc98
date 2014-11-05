CC98
=================

时隔一年之后cc98水贴程序计划再启动,  
看看我和一年前的变化.



required
-------------

requests >= 2.3.0  
support python 3.3+  
compat with python 2.7+


Quickstart
--------------------

simple use  
```python
from cc98 import CC98User
user = CC98User(your_username,your_passwd, ['2333', 'hhhhh'])
user.reply(cc98_url)
```

use file like object:  

```python
from cc98 import CC98User
with open('relpy_contents.txt')as f:
    user = CC98User(your_username,your_passwd, f)
user.reply(cc98_url)
```

Those will random choose a content to post

You can also special assign a reply:    
```python
user.reply(cc98_url, 'your reply')
```

Enjoy!  

To Do
------------
- reply---------------->done
- user strea
- compat with python2  ------------>done
- main

update
-----------
- 登陆成功 ----------------->11-5
- 回复帖子成功 --------------> 11-5 , 17:11
- 兼容python2 --------------> 11-5 , 23:17