#!/usr/bin/env python
# coding=utf-8

import allure
import pytest
from .report import report

# @report.epic("Driver")
# @report.feature('hello')
# class TestShoppingTrolley(object):
#     @report.story('miximixi')
#     class TestInClass():
#         def test_in_test_class(self):
#             pass
#     @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
#     @report.story('hello')
#     def test_add_shopping_trolley(self):
#         login('ss', 'mm')
#         with report.step("mm"):
#             report.attach('', '')
#         with report.step(""):
#             pass
#         with report.step("aa"):
#             report.attach('', 's')
#             assert 'success' == 'failed'

#     @report.testcase("https://issues.sierrawireless.com/browse/QTI9X28-4440")
#     @report.story('mm')
#     def test_edit_shopping_trolley(self):
#         pass

#     @report.mark.skipif(reason='sss')
#     @report.story('aaa')
#     def test_delete_shopping_trolley(self):
#         pass


# @report.step('tt')
# def login(user, pwd):
#     print(user, pwd)

# @report.xfail(condition=lambda: True, reason='this test is expecting failure')
# def test_xfail_expected_failure():
#     """this test is an xfail that will be marked as expected failure"""
#     assert False

# @report.skipif(condition = lambda: True, reason='This test is skipped by a triggered condition in @pytest.mark.skipif')
# def test_skip_by_triggered_condition():
#     pass

# def test_multiple_attachments():
#     report.attach_file('/mnt/sda2/rzheng/__mzPython__/self/test/pytest.ini', attachment_type=report.attachment_type.TEXT)
#     report.attach('<head></head><body> a page </body>', 'Attach with HTML type', report.attachment_type.HTML)

def test_logger(darling_misc):
    darling = darling_misc(__file__,
                           logger_name = "DACIS.testcase",
                           mail_to  = 'rzheng@sierrawireless.com',
                           port_names = [
                               'pi-slave-01..AT',
                               'pi-slave-02..ADB',
                           ])
    darling.log("hello, darling.")

    darling.at.show_conf()
    darling.adb.show_conf()

@pytest.fixture(params=[True, False], ids=['param_true', 'param_false'])
def function_scope_fixture_with_finalizer(request):
    if request.param:
        print('True')
    else:
        print('False')
    def function_scope_finalizer():
        function_scope_step()
    request.addfinalizer(function_scope_finalizer)


@pytest.fixture(scope='class')
def class_scope_fixture_with_finalizer(request):
    def class_finalizer_fixture():
        class_scope_step()
    request.addfinalizer(class_finalizer_fixture)


@pytest.fixture(scope='module')
def module_scope_fixture_with_finalizer(request):
    def module_finalizer_fixture():
        module_scope_step()
    request.addfinalizer(module_finalizer_fixture)


@pytest.fixture(scope='session')
def session_scope_fixture_with_finalizer(request):
    def session_finalizer_fixture():
        session_scope_step()
    request.addfinalizer(session_finalizer_fixture)


class TestClass(object):

    def test_with_scoped_finalizers(self,
                                    function_scope_fixture_with_finalizer,
                                    class_scope_fixture_with_finalizer,
                                    module_scope_fixture_with_finalizer,
                                    session_scope_fixture_with_finalizer):
        step_inside_test_body()


@allure.step
def simple_step(step_param1, step_param2 = None):
    pass


@pytest.mark.parametrize('param1', [True, False], ids=['id explaining value 1', 'id explaining value 2'])
def test_parameterize_with_id(param1):
    simple_step(param1)


@pytest.mark.parametrize('param1', [True, False])
@pytest.mark.parametrize('param2', ['value 1', 'value 2'])
def test_parametrize_with_two_parameters(param1, param2):
    simple_step(param1, param2)


@pytest.mark.parametrize('param1', [True], ids=['boolean parameter id'])
@pytest.mark.parametrize('param2', ['value 1', 'value 2'])
@pytest.mark.parametrize('param3', [1])
def test_parameterize_with_uneven_value_sets(param1, param2, param3):
    simple_step(param1, param3)
    simple_step(param2)

@pytest.fixture
def attach_file_in_module_scope_fixture_with_finalizer(request):
    allure.attach('A text attacment in module scope fixture', 'blah blah blah', allure.attachment_type.TEXT)
    def finalizer_module_scope_fixture():
        allure.attach('A text attacment in module scope finalizer', 'blah blah blah blah',
                      allure.attachment_type.TEXT)
    request.addfinalizer(finalizer_module_scope_fixture)


def test_with_attacments_in_fixture_and_finalizer(attach_file_in_module_scope_finalizer):
    pass


def test_multiple_attachments():
    allure.attach.file('/mnt/sda2/rzheng/__mzPython__/self/darling.pdf', attachment_type=allure.attachment_type.PDF)
    allure.attach('<head></head><body> a page </body>', 'Attach with HTML type', allure.attachment_type.HTML)
    allure.attach('/mnt/sda2/rzheng/__mzPython__/self/test.png', attachment_type = allure.attachment_type.PNG)
