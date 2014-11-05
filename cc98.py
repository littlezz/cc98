#! python3

# python2 compatible
from __future__ import print_function
try:
    from urllib.parse import parse_qsl, parse_qs
except ImportError:
    from urlparse import parse_qsl, parse_qs

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
        # TODO:  compat with python2
        super().__init__()
        self.username = username
        self.passwd = passwd
        self._can_login = False
        self.logged = False
        # username and passwd can not be empty
        if username and passwd:
            self._can_login = True

        self.reply_contents = list(reply_contents) if reply_contents else None
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
        login_head = {'X-Requested-With': 'XMLHttpRequest'}
        res = self.post(self.LOGIN_URL, data=post_form, headers=login_head)
        if res.ok:
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
        assert self.reply_contents or special_reply_content, 'No reply text!'

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
        post_reply = special_reply_content if special_reply_content else random.choice(self.reply_contents)

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
        reply_resp = self.post(reply_url, data=post_form)

        return reply_resp


