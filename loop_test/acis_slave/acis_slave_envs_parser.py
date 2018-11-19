#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author: Shawn Wu
@contact: shwu@sierrawireless.com
@file : acis_slave_envs_parser.py
@time: 2018/10/30 17:06
"""

import os
import re
import acis_slave_port_manager

# parse the string like UART1_COM=r'/dev/ttyUSB1'
# for UART1_COM=r'/dev/ttyUSB1', key is UART1_COM, value is r'/dev/ttyUSB1'
def parse_key_and_value(key_value_string):
    key_value_dict = {}
    
    if key_value_string:
        for i in range(len(key_value_string)):
            index = key_value_string[i].find("=")
            string_len = len(key_value_string[i])
            key_value_dict[key_value_string[i][0:index]] = key_value_string[i][index + 1 : string_len]
    
    return key_value_dict


def get_bool_value(name):
    bool_value = os.getenv(name)
    if "true" == bool_value:
        return True
    else:
        return False
    
    
class Slave_envs_parser:
    def __init__(self):
        dut_port = acis_slave_port_manager.DUTPortManager()
        self.serial_com_string_list = dut_port.get_avilable_at_port()
        self.dm_com_string_list = dut_port.get_available_dm_port()
        self.nmea_com_string_list = dut_port.get_availbale_nmea_port()
        self.adb_id_list = dut_port.get_available_adb_port()
        self.test_script_store_path = ''
        
    # Get test case list
    def get_test_case_list(self):
        return os.getenv("CASENAME")

    # Get test count for each test case
    def get_test_count(self):
        test_count = int(os.getenv("TIMES"))
        return test_count

    # Get platform
    def get_platform(self):
        return os.getenv('PLATFORM')

    # check if test QMI unit test, otherwise test AT unit test.
    def enable_qmi_test(self):
        if os.getenv("TYPES") == 'qmi':
            return True
        else:
            return False
        
    # check if need to update FW
    def enable_update_fw(self):
        return get_bool_value('FW_UPDATE')

    # Get FW version
    def get_FW_ver(self):
        return os.getenv('FW_VERSION')
        
    # Get FW image path
    def get_FW_image_path(self):
        return os.getenv('FW_IMAGE_PATH')

    # Get serial com port string list
    def get_serial_com_string_list(self):
        return self.serial_com_string_list

    # Get serial com port with dict
    # key is port name, value is port number
    # UART1_COM: DUT AT port, UART2_COM: collaborator AT port
    # UART3_COM: DUT serial port, UART4_COM: collaborator serial port
    def get_serial_com_dict(self):
        return parse_key_and_value(self.serial_com_string_list)

    # Get DM COM port string list
    def get_dm_com_string_list(self):
        return self.dm_com_string_list
        
    # Get DM com port with dict
    # key is port name, value is port number
    # DM1_COM: DUT DM port, DM2_COM: collaborator DM port
    def get_dm_com_dict(self):
        return parse_key_and_value(self.dm_com_string_list)
    
    # Get NMEA COM port string list
    def get_nmea_com_string_list(self):
        return self.nmea_com_string_list
    
    # Get NMEA com port with dict
    # key is port name, value is port number
    # NMEA1_COM: DUT NMEA port, NMEA2_COM: collaborator NMEA port
    def get_nmea_com_dict(self):
        return parse_key_and_value(self.nmea_com_string_list)

    # Get adb id string list
    def get_adb_id_string_list(self):
        return self.adb_id_list
    
    # Get adb id with dict
    # key is port name, value is port number
    # TARGET_ADB_ID1: DUT ADB ID, TARGET_ADB_ID2: collaborator ADB ID
    def get_adb_id_dict(self):
        return parse_key_and_value(self.adb_id_list)
    
    # Get the test sciprt store path
    def get_test_script_store_path(self):
        self.test_script_store_path = os.getenv('TESTCASE_PATH')
        return self.test_script_store_path

    def get_test_script_directory_name(self):
        script_directory_name = self.test_script_store_path.split('/')[-2]
        return script_directory_name

    # Get the AT test config file
    def get_at_test_cfg(self):
        return os.getenv('FW_IMAGE_PATH')

    # Get log directory
    def get_log_directory(self):
        return os.getenv('REPORT_PATH') + '/' + os.getenv("PLATFORM") + "/"  + os.getenv("ACIS_DIFF")

    # Get qmi test app path and name
    def get_qmi_testapp_path(self):
        return os.getenv('FW_IMAGE_PATH')

    # Get qmi test configuration file
    def get_qmi_configuration_file(self):
        return self.get_qmi_testapp_path() + '/config_file'

    def get_qmi_log_directory(self):
        if not os.path.exists(self.get_log_directory() + "/QMI"):
            os.makedirs(self.get_log_directory() + "/QMI")
        return self.get_log_directory() + "/QMI"

    def get_qmi_auto_generate_script_path(self):
        if not os.path.exists(self.get_auto_generate_test_script_path() + '/QMI'):
            os.makedirs(self.get_auto_generate_test_script_path() + '/QMI')
        return self.get_auto_generate_test_script_path() + '/QMI'

    def get_auto_generate_test_script_path(self):
        return os.getenv('LOOP_TEST') + '/'  + os.getenv("ACIS_DIFF")

    def get_qmi_testapp(self):
        return self.get_qmi_testapp_path() + '/testQaQmi'
