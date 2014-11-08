# -*- coding: utf-8 -*
#! python3

# python2 compatible
from __future__ import print_function
try:
    from urllib.parse import parse_qsl, parse_qs
except ImportError:
    from urlparse import parse_qsl, parse_qs
    print('检查到python2, 自动启动摧毁系统程序\n, bye~ >_<')
import random
import re
from requests import Session
from requests.compat import urlencode, urlparse
from hashlib import md5

__author__ = 'zz'


class CC98User(Session):
    LOGIN_URL = 'http://www.cc98.org/sign.asp'
    CC98_URL = 'http://www.cc98.org'
    REPLY_BASE_URL = 'http://www.cc98.org/SaveReAnnounce.asp'
    pat_followup_value = re.compile(r'<input.*?followup.*?((?<=value=).*?)>')

    def __init__(self, username=None, passwd=None, reply_contents=None):
        """
        :param reply_contents: filelike obj or list like obj
        """
        super(CC98User, self).__init__()
        self.username = username
        self.passwd = passwd
        self._can_login = False
        self.logged = False

        if username and passwd:
            self._can_login = True

        self._reply_contents = list(reply_contents) if reply_contents else None
        if self._can_login:
            self._login()

        assert self.logged, 'Not login successfully!'
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
        login_head = {'X-Requested-With': 'XMLHttpRequest'}
        self._login_res = self.post(self.LOGIN_URL, data=post_form, headers=login_head)

        # cc98 is too ....
        if self._login_res.text == '9898':
            self.logged = True

        self.headers.update({
            'Agent-User': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36',
            'Origin': 'http://www.cc98.org',
            'Referer': 'http://www.cc98.org/index.asp'
        })

    def reply(self, url, special_reply_content=None):
        """
        :param special_reply_content: will use this reply instead of self.replies
        :return: if success return True, else return False
        """
        assert self.logged, 'Did not login successfully!'
        assert self._reply_contents or special_reply_content, 'No reply text!'

        resp = self.get(url)
        followup_value = self.pat_followup_value.search(resp.text).group(1).strip(r'\"')

        # 为什么不用parse_qs? 因为cc98 url上的boardid有些大写有些小写,不是统一的,
        # cc98 is too SB
        # 为什么不用lower降成小写?因为我写完上面那句话才想起来的,为了保留上面那句话
        # I is too SB
        qs_list = parse_qsl(urlparse(url).query)
        boardid = qs_list[0][1]
        rootid = qs_list[1][1]
        reply_url = self.REPLY_BASE_URL + '?' + urlencode((('method', 'fastreply'), ('BoardID', boardid)))
        cookies_password = parse_qs(resp.request.headers['cookie']).get('password')[0]
        post_reply = special_reply_content if special_reply_content else random.choice(self._reply_contents)

        post_form = {
            'followup':    followup_value,
            'RootID':      rootid,
            'star':        '1',
            'UserName':    self.username,
            'passwd':      cookies_password,
            'Expression':  'face7.gif',
            'Content':     post_reply,
            'signflag':    'yes',
        }
        self._reply_resp = self.post(reply_url, data=post_form)


        return self._reply_resp.ok


def user_flow(usernames=None, passwds=None, reply_contents_=None):
    """
    usage:
        user_stream_reply = user_flow(usernames,passwds,reply_contents)
        user_stream_reply(url)

    """
    reply_contents = list(reply_contents_)
    users = []
    for username, passwd in zip(usernames, passwds):
        try:
            username = username.strip()
            passwd = passwd.strip()
            user = CC98User(username, passwd, reply_contents)
            users.append(user)
        except AssertionError:
            print(username, passwd, 'can not loggin')

    def reply_flow(reply_url):
        for user in users:
            response_status = user.reply(reply_url)
            print(user.username, response_status)

    return reply_flow

if __name__ == '__main__':
    from os.path import join

    def get_path(filename):
        return join('users_info', filename)

    users = []
    with open(get_path('usernames.txt')) as fnames, open(get_path('passwords.txt'))as fpasswds, open(get_path('resp.txt')) as fresp:
        users_reply = user_flow(fnames, fpasswds, fresp)

    with open(get_path('url.txt')) as furl:
        url = furl.read().strip()

    users_reply(url)