#!/usr/bin/python
#encoding=utf8


import json


class GetFromFile(object):
    def __init__(self, fname):
        self.file_ = fname

    def read(self):
        with open(self.file_) as f:
            r = f.read()
        return r if r else None

    def write(self, content):
        with open(self.file_, 'w') as f:
            f.write(content)

    def read_json(self):
        with open(self.file_) as f:
            try:
                r = json.load(f)
            except ValueError:
                r = None
            return r

    def write_json(self, content):
        with open(self.file_, 'w') as f:
            json.dump(content, f)

