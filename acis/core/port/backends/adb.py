#! /usr/bin/env python
# coding=utf-8


"""
"""

class ADB():
    name = 'ADB'
    def __init__(self, conf):
        self.conf = conf

    def whoami(self):
        return "My name is: {name}".format(name = ADB.name)

    def show_conf(self):
        print("I'm {name}, conf is:\n{conf}".format(name = ADB.name, conf = self.conf))
