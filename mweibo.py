#!/usr/bin/python
#encoding=utf8


from weibo import APIClient
from antool import GetFromFile
# import requests


class Weibo(object):
    def __init__(self, app_key, app_secret, session_file='.session'):
        self._session_file = GetFromFile(session_file)
        self.client = None
        self.app_key = app_key
        self.app_secret = app_secret
        self.login()

    def get_session(self):
        return self._session_file.read_json()

    def save_session(self, toxp):
        self._session_file.write_json(toxp)

    def login(self):
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri="http://www.weibo.com")
        session = self.get_session()
        if not session:
            # aurl = self.client.get_authorize_url()
            # print('aurl', aurl)
            # #TODO code is modified
            # rsp = requests.get(aurl)
            self.code = '' # need to get code
            rs = self.client.request_access_token(self.code)
            self.save_session(rs)
        try:
            self.client.set_access_token(session['access_token'], session['expires_in'])
        except Exception as e:
            print(e)
            print('login error')
            exit()
        print('login success')

    def send(self, pic_path, status=u'shaye~'):
        # client.statuses.user_timeline.get()
        with open(pic_path) as pic:
            self.client.statuses.upload.post(status=status, pic=pic)


def main():
    from config import APP_KEY, APP_SECRET
    weibo = Weibo(APP_KEY, APP_SECRET)
    weibo.send(pic_path='/home/soso/Pictures/Selection_036(auto send by shaye ~)_shaye.png', status='test shaye~')


if __name__ == '__main__':
    main()
