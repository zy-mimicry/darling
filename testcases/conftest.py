#!/usr/bin/env python
# coding=utf-8

from .report import report
import os,sys
import pytest, allure

"""
Darling configuration of logs.
"""
current_file = os.path.abspath(__file__)
current_path = os.path.dirname(current_file)
parent_path  = os.path.dirname(current_path)

print("path : ", parent_path)
from .darling_file import darling_mimicry_dir
print("Construct Darling Logs Directory.")
darling_mimicry_dir(parent_path,  # Retrieve the directory structure.
                    parent_path,) # Can configured by yourself, that is log's out-path

print("Logger init")
from .log_test import DarlingTestLogger
@report.fixture()
def dlog():
    return DarlingTestLogger

"""
Darling configuration of port.
"""


"""
pytest common configuration.
"""

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
def darling_pass_fixture():
    assert True

@report.fixture(name = "darling skip")
def darling_skip_fixture():
    pytest.skip()

@report.fixture(name = "darling fail")
def darling_fail_fixture():
    assert False

@report.fixture(name = "darling broken")
def darling_broken_fixture():
    raise Exception("Sorry, it's broken.")


"""
Jenkins environment. TBD.
"""

"""
DataBase. TBD.
"""

