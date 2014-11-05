__author__ = 'zz'

from requests import Session
from hashlib import md5



###################
_LOGIN_URL = 'http://www.cc98.org/sign.asp'
_CC98_URL = 'http://www.cc98.org'



#########################
class CC98User(Session):
    LOGIN_URL = _LOGIN_URL
    CC98_URL = _CC98_URL

    def __init__(self, username=None, passwd=None, replies=None):
        """
        :param username: string
        :param passwd: string
        :param replies: filelike obj or list like obj
        """
        # python3
        super().__init__()
        self.username = username
        self.passwd = passwd
        self._can_login = False
        self.logined = False
        # username and passwd can not be empty
        if username and passwd :
            self._can_login = True

        self.replies = replies if replies else None
        if self._can_login:
            self._login()

    def scan(self, url):
            return self.get(url)

    def _login(self):
        self.scan(self.CC98_URL)
        md5_passwd = md5(self.passwd.encode()).hexdigest()
        post_form = {
            'a': 'i',
            'u': self.username,
            'p': md5_passwd,
            'userhidden': '2',
        }
        login_head={
            'X-Requested-With': 'XMLHttpRequest',
        }
        res = self.post(self.LOGIN_URL, data=post_form, headers=login_head)
        if res.status_code == 200:
            self.logined = True








    def reply(self, url, reply=None):
        """
        :param reply: will use this reply instead of self.replies
        :return: if success return True, else return False
        """
        pass


