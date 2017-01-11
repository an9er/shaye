from weibo import APIClient

class Weibo(object):
    def __init__(self, app_key, app_secret, code):
        self.client = None
        self.app_key = app_key
        self.app_secret = app_secret
        self.code = code
        self.login()

    def login(self):
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri="http://www.weibo.com")

        # client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri="http://www.weibo.com")
        # print client.get_authorize_url()
        # client.access_token

        # my weibo's coressponding code
        r = self.client.request_access_token(self.code)
        access_token = r.access_token # 新浪返回的token，类似abc123xyz456
        expires_in = r.expires_in
        self.client.set_access_token(access_token, expires_in)

    def send(self, pic_path, status=u'shaye~'):
        # client.statuses.user_timeline.get()
        self.client.statuses.upload.post(status=status, pic=open(pic_path))
