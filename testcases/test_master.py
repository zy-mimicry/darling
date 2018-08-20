#!/usr/bin/env python
# coding=utf-8

import allure
import pytest
from .report import report

# @report.epic("xxxxxxxxxxxxxxxxxxxxxx")
# @report.feature('购物车功能')  # feature定义功能
# class TestShoppingTrolley(object):
#     @report.story('miximixi')  # story定义用户场景
#     class TestInClass():
#         def test_in_test_class(self):
#             pass
#     @report.issue("https://issues.sierrawireless.com/browse/QTI9X28-4440","127.0.0.1:8000")
#     @report.story('加入购物车')  # story定义用户场景
#     def test_add_shopping_trolley(self):
#         login('刘春明', '密码')  # 调用“步骤函数”
#         with report.step("浏览商品"):  # 将一个测试用例分成几个步骤，将步骤打印到测试报告中，步骤2
#             report.attach('商品1', '刘春明')  # attach可以打印一些附加信息
#             report.attach('商品2', 'liuchunming')
#         with report.step("点击商品"):  # 将一个测试用例分成几个步骤，将步骤打印到测试报告中，步骤3
#             pass
#         with report.step("校验结果"):
#             report.attach('期望结果', '添加购物车成功')
#             report.attach('实际结果', '添加购物车失败')
#             assert 'success' == 'failed'

#     @report.testcase("https://issues.sierrawireless.com/browse/QTI9X28-4440")
#     @report.story('修改购物车')
#     def test_edit_shopping_trolley(self):
#         pass

#     @report.mark.skipif(reason='本次不执行')
#     @report.story('删除购物车')
#     def test_delete_shopping_trolley(self):
#         pass


# @report.step('用户登录')
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

def test_logger(dlog):
    darling = dlog(__file__,
                   'rzheng@sierrawireless.com')
    darling.log("hello, darling.")
