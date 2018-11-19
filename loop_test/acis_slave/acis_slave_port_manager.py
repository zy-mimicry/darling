#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author: Shawn Wu
@contact: shwu@sierrawireless.com
@file : acis_slave_port_manager.py
@time: 2018/10/31 14:50
"""
import os

# ADB ID should be format like TARGET_ADB_ID1=r'356b945e';TARGET_ADB_ID2=r'356B945e'
def get_all_adb_id():
    adb_id_list = []
    returninfo = os.popen('adb devices')
    i = 1
    while 1:
        try:
            line = returninfo.readline()
            if 'device\n' in line:
                target_id_name = "TARGET_ADB_ID%d" % i
                i = i + 1
                adb_id_list.append(target_id_name + "=r'" + line.split()[0] + "'")
        except:
            continue
        if len(line) <= 0:
            break
    print("All adb ids are: ")
    print(adb_id_list)
    return adb_id_list


def get_ttyUSB_port(port_bus_flag):
    # search the AT com port in the /sys/devices/platform/soc/ directory
    # /sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.5/1-1.5:1.3/ttyUSB5
    # as the example, 1-1.5:1.3 is the AT  com port.
    at_com_list = []
    returninfo = os.popen('find /sys/devices/platform/soc/ -name "ttyUSB*"')
    while 1:
        try:
            line = returninfo.readline()
            if port_bus_flag in line and line.split('/')[-2] != 'tty':
                at_com_list.append(line.split('/')[-2])
        except:
            continue
        if len(line) <= 0:
            break
    return at_com_list


# format the AT com port like UART1_COM=r'1-1.4:1.3'
def format_com_port(port_name, port_bus_flag):
    com_port_list = []
    port_id = get_ttyUSB_port(port_bus_flag)
    i = 1
    for each_port in port_id:
        port_full_name = port_name % i
        i = i + 1
        com_port_list.append(port_full_name + "=r'" + each_port + "'")
    print("All com ports are: ")
    print(com_port_list)
    return com_port_list


def get_at_com_port():
    return format_com_port("UART%d_COM", '1.3/ttyUSB')


def get_nmea_com_port():
    return format_com_port("NMEA%d_COM", '1.2/ttyUSB')


def get_dm_com_port():
    return format_com_port("DM%d_COM", '1.0/ttyUSB')


class DUTPortManager:
    def __init__(self):
        self.adb_available_port = []
        self.at_available_port = []
        self.nmea_available_port = []
        self.dm_available_port = []

    def get_available_adb_port(self):
        self.adb_available_port = get_all_adb_id()
        return self.adb_available_port

    def get_avilable_at_port(self):
        self.at_available_port = get_at_com_port()
        return self.at_available_port

    def get_available_dm_port(self):
        self.dm_available_port = get_dm_com_port()
        return self.dm_available_port

    def get_availbale_nmea_port(self):
        self.nmea_available_port = get_nmea_com_port()
        return self.nmea_available_port
