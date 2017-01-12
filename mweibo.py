#!/usr/bin/python
#encoding=utf8


from weibo import APIClient


class Weibo(object):
    def __init__(self, app_key, app_secret, session_file='./.sesslog'):
        self.client = None
        self.app_key = app_key
        self.app_secret = app_secret
        self.login()
        self._session_file = session_file

    def get_session(self):
        self._session_file.read_json(token, exp)


    def save_session(self, token, exp):
        self._session_file.write_json(token, exp)

    def login(self):
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri="http://www.weibo.com")
        access_token, expires_in = self.get_session()
        if not access_token:
            print(self.client.get_authorize_url())
            #TODO code is modified
            # r = request.
            r = self.client.request_access_token(self.code)
            access_token = r.access_token # 新浪返回的token，类似abc123xyz456
            expires_in = r.expires_in
            self.save_session(access_token, expires_in)
        self.client.set_access_token(access_token, expires_in)

    def send(self, pic_path, status=u'shaye~'):
        # client.statuses.user_timeline.get()
        self.client.statuses.upload.post(status=status, pic=open(pic_path))


def main():
    from config import APP_KEY, APP_SECRET, CODE
    weibo = Weibo(APP_KEY, APP_SECRET, CODE)
    # weibo.login()
    weibo.send(pic_path='/home/soso/Pictures/Selection_036(auto send by shaye ~)_shaye.png', status='test shaye~')


if __name__ == '__main__':
    main()
