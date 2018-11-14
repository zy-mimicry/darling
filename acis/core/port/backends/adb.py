#! /usr/bin/env python
# coding=utf-8


"""
"""

class _ADB():

    def __init__(self):
        print("_ADB instance init.")
    def open(self):pass
    def cmd(self):pass
    def info(self):
        print("I'm _ADB")

class ADB():

    name = 'ADB'

    def __init__(self, obj, conf):

        self.conf = conf

        if obj == "master":
            self.master = _ADB(); return
        elif obj == "slave":
            self.slave = _ADB(); return
        elif obj == "any":
            self.any = _ADB(); return

    def reinit(self, obj, conf):
        print("re-init.")
        self.conf.extend(conf)
        if obj == "master":
            self.master = _ADB()
        else:
            self.slave = _ADB()
        return self

    def whoami(self):
        print("My name is : {name}".format(name = ADB.name))
