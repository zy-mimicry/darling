#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author: Shawn Wu
@contact: shwu@sierrawireless.com
@file : acis_slave_at_testplan_generator.py
@time: 2018/10/31 14:50
"""

import os
import acis_slave_envs_parser
import time
import re
from acis_slave_testplan_generator import Slave_testplan_prepare

def get_test_script_with_full_path(test_case_name, test_script_path):
    test_script = test_case_name + ".py"
    test_script_with_full_path = ''
    for root, dirs, files in os.walk(test_script_path, topdown=True):
        for name in files:
            full_path = os.path.join(root, name)
            if test_script in full_path:
                test_script_with_full_path = full_path
    return test_script_with_full_path


def auto_gernerate_test_function_string():
    testCaseStr = '''
def test_{CASENAME}_{TIMES}(record_xml_attribute):
    record_xml_attribute("classname", "{CASE_RELATIVE_PATH}")
    record_xml_attribute("file", "{CASE_RELATIVE_PATH}/{CASENAME}.py")
    print("***********test_{CASENAME} start*************")
    test_result = False
    res = os.system("python3 {TEST_SCRIPT} -cfg {CFG_FILE} -logpath {LOGPATH}")
    fd = open("{LOGPATH}/{CASENAME}.log",'r')
    logtmp = fd.read()
    if "{CASENAME}: PASSED" in logtmp:
        print("{CASENAME}: PASSED")
        test_result = True
    else:
        print("{CASENAME}: FAILED")
        test_result = False
    fd.close()
    os.rename("{LOGPATH}/{CASENAME}.log", "{LOGPATH}/{CASENAME}_{TIMES}.log")
    assert test_result == True
    print("***********test_{CASENAME} end*************")
'''
    return testCaseStr


def auto_generate_format_script_head():
    # Auto create case file title
    fileStr = '''# _*_ coding: utf-8 _*_

#------------------------------------------------------------------------------------
# @author       Shawn Wu
# @date         2018-11-01
# @Description  Sierra Wireless Test Case
#
# date           who             version             modification
# 2018-11-01     Shawn Wu        1.0                 Creation
#------------------------------------------------------------------------------------
#############################################################################
# Sierra Wireless Test Case
#############################################################################

#############################################################################
# WARNING: Please don't modify manually !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#############################################################################

import os
import pytest


'''
    return fileStr

def get_test_script_relate_path(test_scipt_store_path, test_script_full_path, test_case_name):
    case_relative_store_path_list = test_script_full_path.split(test_scipt_store_path)
    case_relative_store_path_list = case_relative_store_path_list[1].split(test_case_name)
    case_relative_store_path = case_relative_store_path_list[0][0:-1]
    return case_relative_store_path


def set_com_and_adb_port_to_cfg(dynamic_cfg, port_list):
    # read out it first
    fd_dynamic_cfg = open(dynamic_cfg,'r')
    dynamic_cfg_read = fd_dynamic_cfg.read()
    fd_dynamic_cfg.close()
    str_tmp = dynamic_cfg_read

    # Set the port and write back it
    for one_catogory_port_list in port_list:
        # dm_port_list, serial_port_list, nmea_port_list, adb_id_list
        for num in range(len(one_catogory_port_list)):
            fd_dynamic_cfg = open(dynamic_cfg, 'w')
            str_len = one_catogory_port_list[num].find('=')
            str_match = one_catogory_port_list[num][:str_len].strip()
            pattern = r'{str_match}\s*=\s*\w+.\w+.'.format(str_match=str_match)
            str_tmp = re.sub(pattern, one_catogory_port_list[num], str_tmp)
            fd_dynamic_cfg.write(str_tmp)
            fd_dynamic_cfg.close()


def create_dynamic_cfg_with_sample_cfg(sample_cfg, dynamic_cfg):
    fd_sample_cfg = open(sample_cfg, 'r')
    fd_dynamic_cfg = open(dynamic_cfg, 'w+')
    sample_cfg_read_tmp = fd_sample_cfg.read()
    fd_dynamic_cfg.write(sample_cfg_read_tmp)
    fd_dynamic_cfg.close()


def replace_dynamic_cfg_ini_path(dynamic_cfg, ini_path):
    fd_dynamic_cfg = open(dynamic_cfg, 'r')
    tmp_read = fd_dynamic_cfg.read()
    fd_dynamic_cfg.close()

    tmp_read = tmp_read.format(INI_PATH=ini_path)

    fd_dynamic_cfg = open(dynamic_cfg, 'w')
    fd_dynamic_cfg.write(tmp_read)
    fd_dynamic_cfg.close()


class Slave_at_testplan_prepare(Slave_testplan_prepare):
    def __init__(self, ):
        Slave_testplan_prepare.__init__(self)
        self.test_script_with_path = ''
        self.dynamic_cfg = ''
        self.port_list = []
        self.case_relative_store_path = ''

    def search_case(self):
        self.test_script_with_path = get_test_script_with_full_path(self.envs.get_test_case_list(), self.envs.get_test_script_store_path())
        if self.test_script_with_path == '':
            print("@@@@@@@ Erro can't find the test case!")
        return self.test_script_with_path

    def create_pytest_format_script(self):
        test_function_string = auto_gernerate_test_function_string()
        format_script_head = auto_generate_format_script_head()
        format_script = self.auto_generate_script_directory + '/' + self.pytest_format_file_name

        with open(format_script, 'w+') as fd:

            fd.write(format_script_head)

            for times in range(int(self.envs.get_test_count())):
                log_path = self.envs.get_log_directory() + '/' + self.envs.get_test_script_directory_name() + self.case_relative_store_path
                case_function_string = test_function_string.format(CASENAME=self.envs.get_test_case_list(),
                                                                   TEST_SCRIPT=self.test_script_with_path,
                                                                   CFG_FILE=self.dynamic_cfg,
                                                                   LOGPATH=log_path,
                                                                   TIMES=times+1,
                                                                   CASE_RELATIVE_PATH=self.case_relative_store_path)


                fd.write(case_function_string)
            fd.close()

    def create_dynamic_cfg(self):
        self.dynamic_cfg = self.envs.get_auto_generate_test_script_path() + '/' + self.envs.get_test_case_list() + "_dynamic_at.cfg"
        at_test_cfg_sample_file = self.envs.get_at_test_cfg() + '/' + "sample.cfg"

        create_dynamic_cfg_with_sample_cfg(at_test_cfg_sample_file, self.dynamic_cfg)

        replace_dynamic_cfg_ini_path(self.dynamic_cfg, self.envs.get_at_test_cfg())

        self.port_list.append(self.envs.get_serial_com_string_list())
        self.port_list.append(self.envs.get_dm_com_string_list())
        self.port_list.append(self.envs.get_nmea_com_string_list())
        self.port_list.append(self.envs.get_adb_id_string_list())

        set_com_and_adb_port_to_cfg(self.dynamic_cfg, self.port_list)

    def create_auto_generate_script_directory(self):
        self.case_relative_store_path = get_test_script_relate_path(self.envs.get_test_script_store_path(),
                                                               self.test_script_with_path,
                                                               self.envs.get_test_case_list())
        self.auto_generate_script_directory = (self.envs.get_auto_generate_test_script_path() + '/' +
                                               self.envs.get_test_script_directory_name() +
                                               self.case_relative_store_path)


