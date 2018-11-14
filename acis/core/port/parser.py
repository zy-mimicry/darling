#! /usr/bin/env python
# coding=utf-8


"""
"""

from .conf import PI_SLAVE_CONF
from .port_exceptions import *
import os, re

class AcisRuleFileNotExist: pass

class PortConfParser():
    def __init__(self):

        self.configs = {}
        self.udev_conf_file = '/etc/udev/rules.d/11-acis.rules'

    def quick_match(self, backend_name, type_name):
        c = self.configs.get(type_name, None)
        if c:
            if c.get(backend_name, None):
                if backend_name == "AT":
                    return ["/dev/" + self.configs[type_name][backend_name], self.configs[type_name]['serial']]
                elif backend_name == "ADB":
                    return [self.configs[type_name]['serial'], type_name]
        return None

    def slow_match(self, backend_name, type_name):
        return self.pick_info(self.udev_conf_file, backend_name, type_name)

    def get_conf(self, backend_name, type_name):
        conf = self.quick_match(backend_name, type_name)
        if conf: return conf
        conf = self.slow_match(backend_name, type_name)
        return conf

    def pick_info(self,_file, backend_name, type_name):
        if not os.path.exists(_file): raise AcisRuleFileNotExist()
        with open(_file, mode = 'r') as f:
            for line in f:
                g = re.match(r'\s*ATTRS{serial}=="(.*)",\s*GOTO="(.*)\s*"', line)
                if g:
                    if g.group(2) == "acis_master":
                        self.configs["master"] = {"serial" : g.group(1) }
                    elif g.group(2) == "acis_slave":
                        self.configs["slave"]  = {"serial" : g.group(1) }
                g = re.match(r"\s*SUBSYSTEMS==\"usb\",\s*DRIVERS==\"GobiSerial\",\s*SYMLINK\+=\"(acis/(.*))/(.*)\",\s*ATTRS{bInterfaceNumber}==\"(.*)\"\s*", line)
                if g:
                    if g.group(2) == "master":
                        self.configs["master"]["link"] = g.group(1)
                        if g.group(4) == "03":
                            self.configs["master"]["AT"] = g.group(1) + '/' + g.group(3)
                        if g.group(4) == "00":
                            self.configs["master"]["DM"] = g.group(1) + '/' + g.group(3)
                    elif g.group(2) == "slave" :
                        self.configs["slave"]["link"]  = g.group(1)
                        if g.group(4) == "03":
                            self.configs["slave"]["AT"] = g.group(1) + '/' + g.group(3)
                        if g.group(4) == "00":
                            self.configs["slave"]["DM"] = g.group(1) + '/' + g.group(3)

        if backend_name == "AT":
            return ["/dev/" + self.configs[type_name][backend_name], self.configs[type_name]['serial']]
        elif backend_name == "ADB":
            return [self.configs[type_name]['serial'], type_name]