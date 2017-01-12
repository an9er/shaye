#!/usr/bin/python
#encoding=utf8

import os
import time
from mweibo import Weibo
from config import APP_KEY, APP_SECRET, IMG_PATH, TIME_FILE, UPDATE_SNAP
from antool import GetFromFile
import re


class ImgFile(object):
    def __init__(self, name, img_path):
        self.fullname = name
        self.name, self.type_ = self.get_name_type()
        self.img_path = img_path
        self.path = self.get_path()
        self.mdif_time = self.get_modi_time()

    def get_modi_time(self):
        return os.stat(self.path).st_mtime

    def get_path(self):
        if self.img_path.endswith('/'):
            return self.img_path + self.name
        else:
            return self.img_path + '/' + self.name

    def get_name_type(self):
        if self.fullname.endswith('.jpg'):
            ftype = '.jpg'
        if self.fullname.endswith('.png'):
            ftype = '.png'
        name = self.fullname.split(ftype)[-1]
        return name, ftype

    def should_push(self):
        if self.type_ == ('shaye'):
            return True
        return False

    def get_status(self):
        try:
            return re.search('\((.*?)\)', self.name).groups()[0]
        except AttributeError:
            return None


class ShayeScreen(object):
    def __init__(self, app_key, app_secret, img_path, time_file):
        self._imgpath = img_path
        self.weibo = Weibo(app_key, app_secret)
        self.weibo.login()
        self.logtime = GetFromFile(time_file)
        self.lastime = None

    def time_snap(self):
        if not self.lastime:
            self.lastime = time.time()
        now = time.time()
        if now - self.lastime > UPDATE_SNAP:
            return True
        return False

    def get_new_file(self):
        new_imfos = {}
        files = os.listdir(self.img_path)
        #TODO delete pisc a month ago: def delete_a_month(self):
        # fileinfos = [(name, os.stat(self._imgpath+'/'+name).st_mtime) for name in files]
        ifs = [ImgFile(name, self.img_path) for name in files]
        for ifile in ifs:
            if not ifile.should_push():
                continue
            if ifile.mtime > self.lastime:
                finfo = {}
                finfo['path'] = ifile.path
                finfo['status'] = ifile.get_status()
                new_imfos.append(finfo)
        return new_imfos

    def collection(self):
        while 1:
            imfos = self.get_new_file()
            if imfos:
                return imfos
            snap = self.time_snap()
            time.sleep(snap)

    def send_weibo(self, imfos):
        for imfo in imfos:
            path = imfo['path']
            status = imfo['status']
            self.weibo.send(pic_path=path, status=status)

    def start(self):
        while 1:
            imfos = self.collection()
            self.send_weibo(imfos)
            self.logtime.write(time.time())
            self.lastime = time.time()


def main():
    print ('img_path {0}'.format(IMG_PATH))
    shaye = ShayeScreen(APP_KEY, APP_SECRET, IMG_PATH, TIME_FILE)
    shaye.start()


if __name__ == '__main__':
    main()
