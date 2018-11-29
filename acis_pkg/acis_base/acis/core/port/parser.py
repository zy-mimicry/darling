#! /usr/bin/env python
# coding=utf-8


"""
"""

from .conf import PI_SLAVE_CONF
from acis.utils.log import peer
from .port_exceptions import (UnsupportBackendErr,
                              ATdevLinkNotExist,
                              NotFindTypeNameInRule,
                              ATportBusyErr,
                              UnsupportTypeErr,
                              AcisRuleFileNotExist)
import os, re, subprocess
from random import choice


class PortConfParser():

    def __init__(self):

        self.configs = {}

        # any_conf = { "any" : 'master' or 'slave' }
        self.any_conf = {}

        # ACIS udev-configuration Location
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
        Note: Register 'AT' first, then register 'ADB',
        BTW:  MUST register AT port every testcase, if not, ADB can NOT work.

        return   'type_name' : >> 'master' or 'slave' or 'any'
                 'mapto'     : >> only 'any' has this prop.
                 'backend'   : >> 'AT' or 'ADB'
                 'dev_link'  : >> eg: AT > /dev/acis/master/AT
                 'serial_id' : >> adb serial id.
        """

        if type_name == "master":

            if "master" not in self.configs:
                raise NotFindTypeNameInRule("Can NOT find type name <{}> in udev-rules file.".format(type_name))

            if backend_name == "AT":
                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATportBusyErr("AT port is using.")
                if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[type_name][backend_name]))
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'dev_link'  : '/dev/' + self.configs[type_name][backend_name],
                         'serial_id' : self.configs[type_name]["serial"]}
            elif backend_name == "DM":
                raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))
            elif backend_name == "ADB":
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'serial_id' : self.configs[type_name]["serial"]}

        elif type_name == "slave":

            if "slave" not in self.configs:
                raise NotFindTypeNameInRule("Can NOT find type name <{}> in udev-rules file.".format(type_name))

            if backend_name == "AT":
                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATportBusyErr("AT port is using.")
                if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[type_name][backend_name]), shell=True):
                    raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[type_name][backend_name]))
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'dev_link'  : '/dev/' + self.configs[type_name][backend_name],
                         'serial_id' : self.configs[type_name]["serial"]}
            elif backend_name == "DM":
                raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))
            elif backend_name == "ADB":
                return { 'type_name' : type_name,
                         'mapto'     : type_name,
                         'backend'   : backend_name,
                         'serial_id' : self.configs[type_name]["serial"]}

        elif type_name == "any":

            if not self.configs:
                raise NotFindTypeNameInRule("Can NOT find any type names <slave or master> in udev-rules file.")

            if len(self.configs) == 2:

                if backend_name == "AT":
                    sel = choice(["master", "slave"])
                    peer("First get type is {name}".format(name = sel))
                    if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                        peer("Port Busy! Try another...")
                        for another in ["master", "slave"]:
                            if sel != another:
                                if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[another][backend_name]), shell=True):
                                    raise ATportBusyErr("Double AT ports had been using.")
                                else:
                                    if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                                        raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[sel][backend_name]))
                                    self.any_conf[type_name] = another
                                    return { 'type_name' : type_name,
                                            'mapto'      : self.any_conf[type_name],
                                            'backend'    : backend_name,
                                            'dev_link'   : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                                            'serial_id'  : self.configs[self.any_conf[type_name]]["serial"]}
                    else:
                        if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                            raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[sel][backend_name]))
                        self.any_conf[type_name] = sel
                        return {'type_name' : type_name,
                                'mapto'     : self.any_conf[type_name],
                                'backend'   : backend_name,
                                'dev_link'  : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                                'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}

                elif backend_name == "DM":
                    raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))

                elif backend_name == "ADB":
                    return {'type_name' : type_name,
                            'mapto'     : self.any_conf[type_name],
                            'backend'   : backend_name,
                            'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}

            elif len(self.configs) == 1:
                if 'master' in self.configs:
                    if backend_name == "AT":
                        sel = 'master'
                        if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                            raise ATportBusyErr("Only one module register to udev-rules: <{name}>, but this port is using.".format(name = sel))
                        else:
                            if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                                raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[sel][backend_name]))
                            self.any_conf[type_name] = sel
                            return { 'type_name'  : type_name,
                                     'mapto'      : self.any_conf[type_name],
                                     'backend'    : backend_name,
                                     'dev_link'   : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                                     'serial_id'  : self.configs[self.any_conf[type_name]]["serial"]}

                    elif backend_name == "DM":
                        raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))

                    elif backend_name == "ADB":
                        return {'type_name' : type_name,
                                'mapto'     : self.any_conf[type_name],
                                'backend'   : backend_name,
                                'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}

                elif 'slave' in self.configs:

                    if backend_name == "AT":
                        sel = 'slave'
                        if not subprocess.call("lsof {where}".format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                            raise ATportBusyErr("Only one module register to udev-rules: <{name}>, but this port is using.".format(name = sel))
                        else:
                            if subprocess.call('ls {where}'.format(where = '/dev/' + self.configs[sel][backend_name]), shell=True):
                                raise ATdevLinkNotExist("Can NOT find dev-link [{}] for test.".format('/dev/'+self.configs[sel][backend_name]))
                            self.any_conf[type_name] = sel
                            return { 'type_name'  : type_name,
                                     'mapto'      : self.any_conf[type_name],
                                     'backend'    : backend_name,
                                     'dev_link'   : '/dev/' + self.configs[self.any_conf[type_name]][backend_name],
                                     'serial_id'  : self.configs[self.any_conf[type_name]]["serial"]}

                    elif backend_name == "DM":
                        raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))

                    elif backend_name == "ADB":
                        return {'type_name' : type_name,
                                'mapto'     : self.any_conf[type_name],
                                'backend'   : backend_name,
                                'serial_id' : self.configs[self.any_conf[type_name]]["serial"]}

        else:
            raise UnsupportTypeErr("This type that your input [{}] is NOT support now.".format(type_name))
