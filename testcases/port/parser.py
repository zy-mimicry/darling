#! /usr/bin/env python
# coding=utf-8


"""
"""

from .conf import PI_SLAVE_CONF

class PortConfParser():
    def __init__(self):
        self.configs = {} # name unique

    def load(self, name, conf):
        self.configs[name] = conf.get(name) \
            or raise KeyError("[{name} is unvaild slave name.]".format(name = name))
        return self.configs[name]

    def unload(self, name):
        del self.configs[name]

    def quick_match(self, name):
        return self.configs.get(name, None)

    def slow_match(self, name):
        return self.load(name, PI_SLAVE_CONF)

    def get_conf(self, name):
        conf = self.quick_match(name)
        if conf not is None: return conf
        conf = self.slow_match(name)
        return conf

    def display_all(self):
        print("Port Conf List:\n{configs}".format(configs = self.configs))
