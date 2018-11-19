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
import acis_slave_testplan_generator


def qmi_auto_generate_format_script_head():
    qmi_test_plan_head_str = '''
# _*_ coding:utf-8 _*_\n
import os
import re
import time
import pytest\n

'''
    return qmi_test_plan_head_str


def qmi_auto_generate_case_str():
    qmi_test_case_plan_case_str = '''
def test_{CASENAME_FUNC}_{TIMES}(record_xml_attribute):
    record_xml_attribute("classname", "QMI")
    record_xml_attribute("file", "QMI/{CASENAME}.py")
    line = ''
    test_result = False
    print("***********test_{CASENAME}_{TIMES} start*************")

    returninfo = os.popen('adb -s {DEVID} shell "cd /tmp&&./testQaQmi -t {CASENAME}"')
    while 1:
        try:
            line = returninfo.readline()
        except:
            continue
        if len(line) <= 0:
            break

    os.popen('adb -s {DEVID} pull /tmp/te_log/{CASENAME}.log {LOG_PATH}/{CASENAME}_{TIMES}.log')
    time.sleep(2)
    
    fd = open('{LOG_PATH}/{CASENAME}_{TIMES}.log', 'r')
    log_read = fd.read()
    if re.findall(r'>>>>>>>RESULT:Passed:\d+/\d+=100%', log_read):
        test_result = True
    else:
        test_result = False
    print(log_read)
    os.popen('adb -s {DEVID} shell "cd /tmp&&rm /tmp/te_log/* -rf"')
    print("***********test_{CASENAME}_{TIMES} end*************\\n")
    
    fd.close()
    assert test_result == True
'''
    return qmi_test_case_plan_case_str

class Slave_QMI_testplan_prepare(Slave_testplan_prepare):
    def __init__(self, ):
        Slave_testplan_prepare.__init__(self)
        self.adb_id = []
        self.qmi_configuration_file = ''
        self.auto_generate_script_directory = ''

    def push_testapp_to_dut(self):
        # Actually, currently we only can test on one DUT for QMI test
            value = self.envs.get_adb_id_dict()['TARGET_ADB_ID1']
            # remove r,','
            self.adb_id = value[2:-1]
            print('adb -s {TARGET_ADB_ID} push {TEST_APP} /tmp/testQaQmi'.format(TARGET_ADB_ID=self.adb_id, TEST_APP=self.envs.get_qmi_testapp()))
            os.popen('adb -s {TARGET_ADB_ID} push {TEST_APP} /tmp/testQaQmi'.format(TARGET_ADB_ID=self.adb_id, TEST_APP=self.envs.get_qmi_testapp()))

    def create_pytest_format_script(self):
        test_function_string = qmi_auto_generate_case_str()
        format_script_head = qmi_auto_generate_format_script_head()
        format_script = self.envs.get_qmi_auto_generate_script_path() + '/' + self.pytest_format_file_name
        log_path = self.envs.get_qmi_log_directory()
        with open(format_script, 'w+') as fd:
            fd.write(format_script_head)

            for times in range(int(self.envs.get_test_count())):
                # Actually, currently we only can test on one DUT for QMI test, so DEVID = ADB_TARGET_ID1
                case_func = self.envs.get_test_case_list().replace('.', '_')
                case_function_string = test_function_string.format(CASENAME=self.envs.get_test_case_list(),
                                                                   CASENAME_FUNC=case_func,
                                                                   DEVID=self.adb_id,
                                                                   LOG_PATH=log_path,
                                                                   TIMES=times+1)
                fd.write(case_function_string)

            fd.close()

    def push_config_to_dut(self):
        # copy the configuration file to job space
        print('adb -s {TARGET_ADB_ID} push {CONFIG_FILE} /tmp'.format(TARGET_ADB_ID=self.adb_id, CONFIG_FILE=self.envs.get_qmi_configuration_file()))
        os.popen(
            'adb -s {TARGET_ADB_ID} push {CONFIG_FILE} /tmp'.format(TARGET_ADB_ID=self.adb_id, CONFIG_FILE=self.envs.get_qmi_configuration_file()))

    def create_auto_generate_script_directory(self):
        self.auto_generate_script_directory = self.envs.get_qmi_auto_generate_script_path()




