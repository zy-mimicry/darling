#! /usr/bin/env python
# coding=utf-8


"""
"""

from .conf import PI_SLAVE_CONF
from .port_exceptions import *
import os, re, subprocess
from random import choice

class AcisRuleFileNotExist: pass

class PortConfParser():
    def __init__(self):

        self.configs = {}

        self.any_conf = {}
        self.udev_conf_file = '/etc/udev/rules.d/11-acis.rules'

        self._pick_info(self.udev_conf_file)

    def _pick_info(self,_file):
        """
        Pick some information from '_file'
        'self.configs' content:
        eg.
        {
        "master" : { "serial" : xxx,
                     "link"   : xxx, << acis/master
                     "AT"     : xxx, << acis/master/AT
                     "DM"     : xxx},<< acis/master/DM

        "slave" : { "serial"  : xxx,
                     "link"   : xxx, << acis/slave
                     "AT"     : xxx, << acis/slave/AT
                     "DM"     : xxx},<< acis/slave/DM
        }

        """

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

    def get_conf(self, backend_name, type_name):
        """
        Note: Register 'AT' first, then register 'ADB'.
        return   'type_name' : >> 'master' or 'slave' or 'any'
                 'mapto'     : >> only 'any' has this prop.
                 'backend'   : >> 'AT' or 'ADB'
                 'dev_link'  : >> eg: AT > /dev/acis/master/AT
                 'serial_id' : >> adb serial id.
        """

        if type_name == "master":
            if backend_name == "AT":
                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATportBusyErr("AT port is using.")
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'dev_link'  : '/dev/' + self.configs[type_name][backend_name],
                         'serial_id' : self.configs[type_name]["serial"]}
            elif backend_name == "DM":
                print("DM backend, NOT support now")
            elif backend_name == "ADB":
                print("ADB backend, don't care use-status, this can be opened by mutile-user.")
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'serial_id' : self.configs[type_name]["serial"]}

        elif type_name == "slave":
            if backend_name == "AT":
                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATportBusyErr("AT port is using.")
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'dev_link'  : '/dev/' + self.configs[type_name][backend_name],
                         'serial_id' : self.configs[type_name]["serial"]}
            elif backend_name == "DM":
                print("DM backend, NOT support now")
            elif backend_name == "ADB":
                print("ADB backend, don't care use-status, this can be opened by mutile-user.")
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'serial_id' : self.configs[type_name]["serial"]}

        elif type_name == "any":
            if backend_name == "AT":
                sel = choice(["master", "slave"])
                print("get sel is <<<", sel)
                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                    print("port using... try another...")
                    for another in ["master", "slave"]:
                        if sel != another:
                            if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[another][backend_name]), shell=True):
                                raise ATportBusyErr("Another AT port also is using.")
                            else:
                                self.any_conf[type_name] = another
                                return { 'type_name' : type_name,
                                        'mapto'      : self.any_conf[type_name],
                                        'backend'    : backend_name,
                                        'dev_link'   : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                                        'serial_id'  : self.configs[self.any_conf[type_name]]["serial"]}
                else:
                    self.any_conf[type_name] = sel
                    return {'type_name' : type_name,
                            'mapto'     : self.any_conf[type_name],
                            'backend'   : backend_name,
                            'dev_link'  : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                            'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}
            elif backend_name == "DM":
                print("DM backend, NOT support now")
            elif backend_name == "ADB":
                print("ADB backend, nothing do this, this can be opened by mutile-user.")
                return { 'type_name' : type_name,
                         'mapto'     : self.any_conf[type_name],
                         'backend'   : backend_name,
                         'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}
        else:
            raise UnsupportTypeErr("This type that your input [{}] is NOT support now.".format(type_name))
