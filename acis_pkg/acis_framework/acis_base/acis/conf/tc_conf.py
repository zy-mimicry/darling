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
    if os.getenv('JOB_NAME',None) is None:
        # Now, we hope default.
        os.environ['TESTCASE_CFG'] = '/home/jenkins/nfs_acis/Integration_Test/acis_testcases/acis_testcases.cfg'
    else:
        os.environ['TESTCASE_CFG'] = '/home/jenkins/nfs_acis/' + os.environ['JOB_NAME'] + '/acis_testcases/acis_testcases.cfg'

cfile = open(os.environ['TESTCASE_CFG'], 'r')
strings = cfile.read().replace('\\', '/')
cfile.close()

strings = strings.format(INI_PATH = os.path.dirname(os.environ['TESTCASE_CFG']))

exec(compile(strings, 'tc_conf', 'exec'))

del strings
del cfile

