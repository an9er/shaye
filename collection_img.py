#!/usr/bin/python
#encoding=utf8

import os
import time
from weibo import APIError
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
        # print (self.name, self.type_, self.fullname, self.path)
        self.st_mtime = self.get_st_mtime()

    def get_st_mtime(self):
        return os.stat(self.path).st_mtime

    def get_path(self):
        if self.img_path.endswith('/'):
            return self.img_path + self.fullname
        else:
            return self.img_path + '/' + self.fullname

    def get_name_type(self):
        #TODO replace with re
        if self.fullname.endswith('.jpg'):
            ftype = '.jpg'
        elif self.fullname.endswith('.png'):
            ftype = '.png'
        else:
            ftype = '.xxx'
        name = self.fullname.replace(ftype, '')
        return name, ftype

    def should_push(self):
        if self.name.endswith('shaye'):
            return True
        return False

    def get_status(self):
        try:
            return re.search('\((.*?)\)', self.name).groups()[0]
        except AttributeError:
            return None


class ShayeScreen(object):
    def __init__(self, app_key, app_secret, img_path, time_file, update_snap=60*10):
        self.snap = update_snap
        self.weibo = Weibo(app_key, app_secret)
        self.img_path = img_path
        self.logtime = GetFromFile(time_file)
        self.lastime = float(self.logtime.read())

    def time_snap(self):
        if not self.lastime:
            self.lastime = time.time()
        now = time.time()
        snap = now - self.lastime

        return 0 if snap > UPDATE_SNAP else UPDATE_SNAP - snap

    def get_new_file(self):
        new_imfos = []
        files = os.listdir(self.img_path)
        #TODO delete pisc a month ago: def delete_a_month(self):
        # fileinfos = [(name, os.stat(self._imgpath+'/'+name).st_mtime) for name in files]
        ifs = [ImgFile(name, self.img_path) for name in files]
        for ifile in ifs:
            if not ifile.should_push():
                continue
            if ifile.st_mtime > self.lastime:
                print ('here', ifile.name)
                print('st_mtime', time.localtime(ifile.st_mtime))
                finfo = {}
                finfo['path'] = ifile.path
                finfo['status'] = ifile.get_status()
                new_imfos.append(finfo)
        return new_imfos

    def collection(self):
        while 1:
            imfos = self.get_new_file()
            print('find new img {0}'.format(len(imfos)))
            if imfos:
                return imfos
            # snap = self.time_snap()
            print('need to snap {0}'.format(self.snap))
            time.sleep(self.snap)

    def send_weibo(self, imfo):
        path = imfo['path']
        status = imfo['status']
        try:
            self.weibo.send(pic_path=path, status=status)
            print('file {0} send success!'.format(path))
        except APIError as e:
            print(e)

    def start(self):
        while 1:
            imfos = self.collection()
            for imfo in imfos:
                self.send_weibo(imfo)
                self.logtime.write(str(time.time()))
                print('logtime done')
                self.lastime = time.time()
                print('take a 10s snap')
                time.sleep(10)


def main():
    print('img_path {0}'.format(IMG_PATH))
    shaye = ShayeScreen(APP_KEY, APP_SECRET, IMG_PATH, TIME_FILE, update_snap=UPDATE_SNAP)
    shaye.start()


if __name__ == '__main__':
    main()
