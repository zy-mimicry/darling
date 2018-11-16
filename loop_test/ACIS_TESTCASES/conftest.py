#!/usr/bin/env python
# coding=utf-8

#from .report import report
import time
import os,sys
import pytest, allure

current_file = os.path.abspath(__file__)
current_path = os.path.dirname(current_file)
parent_path  = os.path.dirname(current_path)

print("Location:\n-file:{}\n-current path:{}\n-parent path: {}".
      format(current_file,
             current_path,
             parent_path))

# nfs_mounted_path = '/mnt/sda2/rzheng/__mzPython__/self/wawawa' # must exist!
different_str = time.strftime('%Y_%m_%d_%H_%M_%S') # from environment.

#from . import darling_file

print("-- Construct Darling Logs Directory.")
#darling_file.different_str = different_str
prefix_of_log_path = parent_path + '/' + 'darling_log/' + different_str

import acis
from acis.core.report import  report

#mdarling = acis.ACISMiscer(prefix_of_log_path)
mdarling = acis.ACISMiscer()

@report.fixture(scope="module")
def darling_misc():
    return mdarling.misc_deal

@report.fixture(scope='function')
def function_scope_fixture_with_finalizer(request):
    def function_finalizer_fixture():
        function_scope_step()
    request.addfinalizer(function_finalizer_fixture)


@report.fixture(scope='class')
def class_scope_fixture_with_finalizer(request):
    def class_finalizer_fixture():
        class_scope_step()
    request.addfinalizer(class_finalizer_fixture)


@report.fixture(scope='module')
def module_scope_fixture_with_finalizer(request):
    def module_finalizer_fixture():
        module_scope_step()
    request.addfinalizer(module_finalizer_fixture)


@report.fixture(scope='session')
def session_scope_fixture_with_finalizer(request):
    def session_finalizer_fixture():
        session_scope_step()
    request.addfinalizer(session_finalizer_fixture)

# If needed, use it.
@report.fixture(params=[True, False], ids=['param_true', 'param_false'])
def function_scope_fixture_with_finalizer(request):
    if request.param:
        print('True')
    else:
        print('False')
    def function_scope_finalizer():
        function_scope_step()
    request.addfinalizer(function_scope_finalizer)

@report.fixture(name = "darling pass")
def acis_pass_fixture():
    assert True

@report.fixture(name = "darling skip")
def acis_skip_fixture():
    pytest.skip()

@report.fixture(name = "darling fail")
def acis_fail_fixture():
    assert False

@report.fixture(name = "darling broken")
def acis_broken_fixture():
    raise Exception("Sorry, it's broken.")
