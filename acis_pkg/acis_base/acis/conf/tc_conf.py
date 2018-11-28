#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODO:

1. Read file context to this module.
2. Join the 'INI_PATH' to strings from file.
3. execute string and make it to be a module.

Note: If you want to know what contains in this module, please check the 'acis_testcases.cfg' file.

"""

import os

if os.getenv('TESTCASE_CFG', None) == None:
    os.environ['TESTCASE_CFG'] = '/home/jenkins/nfs_acis/Integration_Test/acis_testcases/acis_testcase.cfg'

cfile = open(os.environ['TEST_CFG_PATH'], 'r')
strings = cfile.read().replace('\\', '/')
cfile.close()

strings = strings.format(INI_PATH = os.path.dirname(os.environ['TEST_CFG_PATH']))

exec(compile(strings, 'tc_conf', 'exec'))

del strings
del cfile

