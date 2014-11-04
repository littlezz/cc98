__author__ = 'zz'

from requests import Session
from hashlib import md5



###################
LOGIN_URL = 'http://www.cc98.org/sign.asp'
CC98_URL = 'http://www.cc98.org'



#########################
class CC98User(Session):



    def __init__(self, username=None, passwd=None, usernamefile=None, passwdfile=None, replies=None):
        """
        :param username: string
        :param passwd: string
        :param usernamefile: filelike obj
        :param passwdfile: filelike obj
        :param replies: filelike obj or list like obj
        """
        # python3
        super().__init__()
        self.usernames = []
        self.passwds = []
        self._can_login = True
        if usernamefile and passwdfile:
            for username_ , passwd_ in zip(usernamefile,passwdfile):
                self.usernames.append(username_)
                self.passwds.append(passwd_)
        elif username and passwd:
            self.usernames.append(username)
            self.passwds.append(passwd)
        else:
            self._can_login = False

        self.replies = replies if replies else None

        if self._can_login:
            self._login()

    def _login(self):
        self.scan(CC98_URL)
        for username, passwd in zip(self.usernames, self.passwds):
            md5_passwd = md5(passwd.encode()).hexdigest()
            post_form = {
                'a': 'i',
                'u': username,
                'p': md5_passwd,
                'userhidden': '2',
            }






    def scan(self, url):
        return self.get(url)

    def reply(self, url, reply=None):
        """
        :param reply: will use this reply instead of self.replies
        :return: if success return True, else return False
        """
        pass


