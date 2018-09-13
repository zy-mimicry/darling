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

def test_logger(mydarling):
    darling = mydarling(__file__,
                        mail_to  = 'rzheng@sierrawireless.com',
                        port_names = [
                            'pi-slave-01..AT',
                            'pi-slave-02..ADB',
                        ])
    darling.log("hello, darling.")
    print(darling.at.whoami())
    darling.at.show_conf()
    darling.adb.show_conf()
