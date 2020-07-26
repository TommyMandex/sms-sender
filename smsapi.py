import string

import requests
import random
import os
import sys
import json

class SMSSender:
    def __init__(self):
        self._url_base = 'http://vvip-sms.com:9800/bulksms'
        self._username = 'test'
        self._password = '12341234'
        self._mt = '1'
        self._fl = '1'
        self._sid = '7781231234'
        self._mno = '19059207942'
        self._msg = 'apitest2'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def url_base(self):
        return self._url_base

    @url_base.setter
    def url_base(self, url):
        self._url_base = url

    @property
    def mt(self):
        return self._mt

    @mt.setter
    def mt(self, mt):
        self._mt = mt

    @property
    def fl(self):
        return self._fl

    @fl.setter
    def fl(self, fl):
        self._fl = fl

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def mno(self):
        return self._mno

    @mno.setter
    def mno(self, mno):
        self._mno = mno

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def fl(self, msg):
        self._msg = msg

    def send(self, username, password, sid, mno, msg):
        endpoint = self._url_base + \
               '?username=' + username + \
               '&password=' + password + \
               '&mt=' + self._mt + \
               '&fl=' + self._fl + \
               '&sid=' + sid + \
               '&mno=' + mno + \
               '&msg=' + msg
        return requests.get(url = endpoint)

class CellReader:
    def read(self, file_name):
        with open(file_name, "r") as f:
            return [line.rstrip() for line in f]


def sms_error_codes_read(file_name):
    with open(file_name) as f:
        return json.load(f)

if __name__ == '__main__':
    '''
    sender = SMSSender()
    sid = '821051134838'
    mno = '19059207942'
    msg = 'apitest'
    for i in range (0, 2):
        msg += str(i)
        sender.send(sid, mno, msg)
    '''
    if len(sys.argv) < 3:
        sys.exit('invalid arguments. try it again: smsapi id password "hello this is a message"')
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        msg = sys.argv[3]

    sender = SMSSender()
    sid = 7781231234
    error_codes = sms_error_codes_read('sms_error_codes.json')
    letters = string.ascii_lowercase

    cr = CellReader()
    cellnumbers_filename = 'cellnumbers.txt'
    cellnumbers = cr.read(cellnumbers_filename)

    for mno in cellnumbers:
        sid += 1
        rt =  ''.join(random.choice('0123456789') for i in range(5))
        # print(str(sid) + ' ' +  mno + ' ' + msg + '  ' + rt)
        ret = sender.send(username, password, str(sid), mno, msg + '  ' + rt)
        ret_code = ret.content.decode('utf-8')
        if (ret_code.split(':')[0] == 'OK'):
            print(mno + ': ' + ret_code)
        else:
            print(mno + ": failed due to " + error_codes[ret_code])
