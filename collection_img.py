#!/usr/bin/python
#encoding=utf8

import os
import time
from weibo import Weibo
from config import APP_KEY, APP_SECRET, CODE, IMG_PATH, TIME_FILE, UPDATE_SNAP


timeinfo = GetFromFile(TIME_FILE)
def time_is_right():
    lastime = timeinfo.read()
    now = time.time()
    if now - lastime > UPDATE_SNAP:
        return True
    return False


def fil_end_with_shaye(fil):
    if fil_get_name(fil).fil_end_with('shaye'):
        return True
    return False


def _get_file():
    new_imgs = []
    lastime = timeinfo.read()
    files = os.listdir(IMG_PATH)
    for fil in files:
        if file_moditime > lastime:
            if fil_end_with_shaye(fil):
                finfo = {}
                finfo['path'] = ??
                finfo['status'] = get_status_via_fname(fil)
                new_imgs.append(fil)
    return new_imgs


def collect_new_imgs():
    while 1:
        if time_is_right():
            return _get_file()


def collection(img_path):
    if time_is_right():
        imgs = collect_new_imgs()
        return imgs


def main():
    weibo = Weibo(APP_KEY, APP_SECRET, CODE)
    imgs = collection()
    weibo.send(imgs)
