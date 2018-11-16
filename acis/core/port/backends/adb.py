#! /usr/bin/env python
# coding=utf-8


"""
"""

import subprocess
from datetime import datetime

class _ADB():

    name = '_ADB'

    def __init__(self, serial_id):

        self.serial_id = serial_id

    def __repr__(self):
       return "<Class: {name} , serial id: {conf}>".format(name = _ADB.name,conf=self.serial_id)

    def send_cmd(self, command, timeout=10):

        try:
            start_time = datetime.now()
            dt = datetime.now()
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Snd"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)

            cmd = 'adb -s %s shell %s' % (self.serial_id, command)
            print(timeDisplay + " ADB " + self.serial_id + " ["+ cmd + "]")

            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
            output = p.communicate()[0]

            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Rcv"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            for each_line in output.split('\n'):
                print(timeDisplay + " ADB "+ self.serial_id + " ["+ each_line.replace("\r","<CR>").replace("\n","<CR>") +"]"+" @"+str(diff_time_ms)+" ms ")
            return output
        except Exception as e:
            print(e)
            print("----->Problem: Exception comes up when send command !!!")
            return "\r\nERROR\r\n"

class ADB():

    name = 'ADB'

    def __init__(self, obj, conf):

        self.conf = {}

        if obj == "master":
            self.conf["master"] = conf
            self.master = _ADB(conf['serial_id']); return
        elif obj == "slave":
            self.conf["slave"] = conf
            self.slave = _ADB(conf['serial_id']); return
        elif obj == "any":
            self.conf["any"] = conf
            self.any = _ADB(conf['serial_id']); return

    def reinit(self, obj, conf):

        if obj == "master":
            self.conf["master"] = conf
            self.master = _ADB(conf['serial_id'])
        else:
            self.conf["slave"] = conf
            self.slave = _ADB(conf['serial_id'])
        return self

    def info(self):
        print("My name is : {name}\n- conf:\n{conf}".format(name = ADB.name, conf = self.conf))
