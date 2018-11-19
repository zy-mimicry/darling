#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author: Shawn Wu
@contact: shwu@sierrawireless.com
@file : acis_slave_testplan_generator.py
@time: 2018/10/31 14:50
"""

import os
import acis_slave_envs_parser
import time
import re
#import acis_at
from acis import ACISMiscer

m = ACISMiscer


def get_port_value(port_dict, port_key):
    return port_dict[port_key]


def get_dut_information(serial_com):
    # Remove the serial_com string begin and end ''
    serial_com = serial_com[2:-1]

    UART = acis_at.AcisOpen(serial_com)
    acis_at.AcisSendAT(UART, "ATI\r")
    response1 = acis_at.AcisWaitResp(UART, ["*\r\nOK\r\n"], 4000)

    acis_at.AcisSendAT(UART, "ATI8\r")
    response2 = acis_at.AcisWaitResp(UART, ["*\r\nOK\r\n"], 4000)

    response = response1 + response2
    acis_at.AcisClose(UART)
    return response


def image_update(uart_port, target_adb_id, image_file, image_version, platform):
    dut_information = get_dut_information(uart_port)

    # remove targe_id 'r '
    target_adb_id = target_adb_id[2:-1]
    if platform not in dut_information:
        print("Error, Platform Conflict")
        raise Exception("Fw update: Error, Platform Conflict")

    if image_version in dut_information:
        print("fw version is expected, no need to update")
        return True
    else:
        os.popen(
            'adb -s {TARGET_ADB_ID} reboot-bootloader & fastboot flash sierra-dual-system {FW_File} & fastboot reboot'.format(
                TARGET_ADB_ID=target_adb_id, FW_File=image_file))

    acis_at.AcisSleep(90000)

    # check if update success
    dut_information = get_dut_information(uart_port)

    if image_version in dut_information:
        print("fw image update successed")
        return True
    else:
        print("fw update failed for" + image_version)
        raise Exception("image update Failed")


class Slave_testplan_prepare:
    def __init__(self):
        self.envs = acis_slave_envs_parser.Slave_envs_parser()
        self.fw_image_file = ''
        self.pytest_format_file_name = "test_" + self.envs.get_test_case_list().replace('.', '_') + ".py"

    def set_fw_image_file(self):
        fw_image_path = self.envs.get_FW_image_path()
        fw_image_name = ''
        file_list = os.listdir(fw_image_path)
        for file_item in file_list:
            if not file_item.endswith('.cwe'):
                continue
            if ('spkg' in file_item) and (fw_image_name == ''):
                fw_image_name = file_item
        if fw_image_name == '':
            print("Can't find FW image")
        else:
            self.fw_image_file = self.envs.get_FW_image_path() + '/' + fw_image_name

    def fw_image_update(self):
        for each in range(len(self.envs.get_adb_id_string_list())):
            port_index = each + 1
            serial_com_dict_key = ("UART%d_COM" % port_index)
            target_adb_id_key = ("TARGET_ADB_ID%d" % port_index)

            UART_COM = get_port_value(self.envs.get_serial_com_dict(), serial_com_dict_key)
            target_adb_id = get_port_value(self.envs.get_adb_id_dict(), target_adb_id_key)
            image_update(UART_COM, target_adb_id, self.fw_image_file, self.envs.get_FW_ver(), self.envs.get_platform())


    def run_pytest(self):
        os.system('pytest -v {AUTO_GENERATE_SCRIPT_PATH}/{TEST_MOUDLE} --junitxml={REPORT_PATH}.xml'.format(
                AUTO_GENERATE_SCRIPT_PATH=self.auto_generate_script_directory,
                TEST_MOUDLE=self.pytest_format_file_name,
                REPORT_PATH=self.envs.get_log_directory() + '/' + self.envs.get_test_case_list().replace('.', '_')))
        # os.system('pytest -v {AUTO_GENERATE_SCRIPT_PATH}/{TEST_MOUDLE} --alluredir {REPORT_PATH}'.format(
        #     AUTO_GENERATE_SCRIPT_PATH=self.auto_generate_script_directory,
        #     TEST_MOUDLE=self.pytest_format_file_name,
        #     REPORT_PATH=self.envs.get_log_directory()))
