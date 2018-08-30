#! /usr/bin/env python
# coding=utf-8


"""
"""

class AT():
    name = "AT"
    def __init__(self, conf):
        self.conf = conf
        pass
    def whoami(self):
        return "My name is: {name}".format(name = AT.name)

    def show_conf(self):
        print("I'm {name}, conf is:\n{conf}".format(name = AT.name, conf = self.conf))

    pass
