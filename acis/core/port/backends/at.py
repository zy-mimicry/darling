#! /usr/bin/env python
# coding=utf-8


"""
"""

class _AT():

    def __init__():
        print("_AT instance init.")
        pass

    def open():
        pass

    def cmd():
        pass

    pass


class AT():

    name = "AT"

    def __init__(self, obj, conf):

        self.conf = conf
        self.obj_name = obj

        if obj == "master":
            self.master = _AT(); return
        elif obj == "slave":
            self.slave = _AT(); return
        elif obj == "any":
            self.any = _AT(); return

    def reinit(self, obj, conf):
        print("re-init.")
        if obj == "master":
            self.master = _AT()
        else:
            self.slave = _AT()
        return self

    def whoami(self):
        return "My name is: {name}".format(name = AT.name)

    def show_conf(self):
        print("I'm {name}, conf is:\n{conf}".format(name = AT.name, conf = self.conf))
