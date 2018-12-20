#! /usr/bin/env python3
# coding=utf-8

"""
< For Rex Debug >
"""

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import json


FT_TABLE = {
    'ERD_ID' : '',
    'L1_Ticket' : '',
    'L2_Ticket' : '',
    'JIRA_BUG_Tickets' : {},
    'TestCases' : {},
    'TestReports' : {},
    'Description' : '',
    'Version' : '',
    'HLD' : '',
    'Age' : '',
    'Action' : '',
    'Status' : '',
    'LastModifier' : '',
    'History' : '',
    'Platform' : '',
}

from .test_cookies_of_rex import random_gen_cookies


def rex_jump(request):

    FT_TABLE['ERD_ID'] = '100'
    FT_TABLE['L1_Ticket'] = 'QTI9X28-5555'
    FT_TABLE['L2_Ticket'] = 'QTI9X28-6666'
    FT_TABLE['JIRA_BUG_Tickets'] = {'first' :'QTI9X28-1234', 'second' : 'QTI9X28-5655'}
    FT_TABLE['TestCases'] = {'first' : 'ACIS_FIRST_TEST_CASE', 'second' : "ACIS_SECOND_TEST_CASE"}
    FT_TABLE['TestReports'] = {'first' : 'ACIS_FIRST_TEST_CASE_REPORT', 'second' : "ACIS_SECOND_TEST_CASE_REPORT"}
    FT_TABLE['Description'] = 'Description Link'
    FT_TABLE['Version'] = '2.0.1'
    FT_TABLE['HLD'] = 'HLD Link here'
    FT_TABLE['Age'] = '2018-12-19'
    FT_TABLE['Action'] = 'new'
    FT_TABLE['Status'] = 'undo'
    FT_TABLE['LastModifier'] = 'Rex Zheng'
    FT_TABLE['History'] = '2.0.100'
    FT_TABLE['Platform'] = 'SD55'


    splitter('save',
             get_cookies = random_gen_cookies,
             pick_erd_list = {'erd_list' : [], 'types' : []})

    return render(request, 'LigerUI/ACIS/rex_test_page.htm', {'cookies' : json.dumps([FT_TABLE])})



def splitter(action, get_cookies = None, pick_erd_list = {'erd_list' : [], 'types' : []}):
    """
    action: 'save', 'pick'

    callback: get_cookies > provide cookies
    get_cookies return:  [{'ERD_ID'  : "",'excel' : {}, 'jira' : {}, 'jenkins' : {}, 'UIform' : {}}, ...]

    pick_erd_list: {'erd_list' : [], 'types' : [] }

    Support Types:
    1. Data from/to Excel
    2. Data from/to JIRA Ticket
    3. Data from/to Jenkins
    4. Data from/to UI Form

    """
    types = {'excel'    : ExcelDataProcesser,
             'jira'     : JiraDataProcesser,
             'jenkins'  : JenkinsDataProcesser,
             'UIform'   : UiFormDataProcesser}

    if action == 'save':
        if not get_cookies:
            print("[get_cookies] callback function is NOT supported.")
            return
        for cookie in get_cookies():
            ERD_ID = cookie.pop('ERD_ID')
            for tp in cookie:
                if tp in types and cookie[tp]:
                    types[tp](ERD_ID, cookies = cookie[tp]).doit(action)

    elif action == 'pick':
        if not pick_erd_list['erd_list']:
            print("[pick_erd_list['erd_list']] is empty]")
            return
        # out_data > eg. {'ERD_ID' : {'jira': data, 'excel' : data, 'jenkins' : data, 'UIform' : data}}
        out_data = {}
        for ERD_ID in pick_erd_list['erd_list']:
            out_data[ERD_ID] = {}
            for tp in pick_erd_list['types']:
                if tp in types:
                    out_data[ERD_ID][tp] = types[tp](ERD_ID).doit(action)
        return out_data
    else:
        print("Action NOT support.")


class CookiesProcesser:

    def save(self):
        assert False, "Children Should implement this method."

    def pick(self):
        assert False, "Children Should implement this method."

    def doit(self):
        assert False, "Children Should implement this method."

dynamic_conf_category = {
    'excel' : (
        'erd_id',
        'category',
        'title',
        'description',
        'product_priority',
        'author',
        'version'),
    'jira' : (
        'HLD',
        'status',
        'l1_jira',
        'l2_jira',
        'bug_jiras',
        'platform',
        'workload',
        'case_name',
        'case_age',
        'report_path',
    ),
    'jenkins' : (
        'fw_version',
        'test_result',
        'test_log',
        'date',
    ),
    'UIform' :(
        'UItest',
    ),
}

from .models_of_rex import Erds

class ExcelDataProcesser(CookiesProcesser):

    data_category = dynamic_conf_category['excel']

    def __init__(self, ERD_ID, cookies = {}, ERD_model = Erds):
        self.ERD_ID = ERD_ID
        self.cookies = cookies
        self.ERD_model = ERD_model

    def save(self):
        '''
        auto ignore the data outof 'data_category'.
        '''
        save_list = []
        except_list = []
        if not self.cookies:
            print("cookies is empty, do nothing.");return
        for c in self.cookies:
            if c in ExcelDataProcesser.data_category:
                save_list.append(c)
            else:
                except_list.append(c)
        for e in except_list:
            self.cookies.pop(e)

        # try:
        #     e = Erds.objects.get(erd_id =self.ERD_ID)
        # except DoesNotExist:
        #     e = Erds.

        e = Erds(**self.cookies)
        e.save()

    def pick(self):
        pass

    def doit(self,action):
        if action == 'save':
            self.save()
        elif action == 'pick':
            return self.pick()

class JiraDataProcesser(CookiesProcesser):

    data_category = dynamic_conf_category['jira']

    def __init__(self, ERD_ID, cookies = {}, ERD_model = Erds):
        self.ERD_ID = ERD_ID
        self.cookies = cookies
        self.ERD_model = ERD_model

    def save(self):
        '''
        auto ignore the data outof 'data_category'.
        '''
        save_list = []
        except_list = []
        if not self.cookies:
            print("cookies is empty, do nothing.");return
        for c in self.cookies:
            if c in JiraDataProcesser.data_category:
                save_list.append(c)
            else:
                except_list.append(c)
        for e in except_list:
            self.cookies.pop(e)

        #e = Erds(**self.cookies)
        #e.save()

    def pick(self):
        pass

    def doit(self,action):
        if action == 'save':
            self.save()
        elif action == 'pick':
            return self.pick()

class JenkinsDataProcesser(CookiesProcesser):

    data_category = dynamic_conf_category['jenkins']

    def __init__(self, ERD_ID, cookies = {}, ERD_model = Erds):
        self.ERD_ID = ERD_ID
        self.cookies = cookies
        self.ERD_model = ERD_model

    def save(self):
        '''
        auto ignore the data outof 'data_category'.
        '''
        save_list = []
        except_list = []
        if not self.cookies:
            print("cookies is empty, do nothing.");return
        for c in self.cookies:
            if c in JenkinsDataProcesser.data_category:
                save_list.append(c)
            else:
                except_list.append(c)
        for e in except_list:
            self.cookies.pop(e)

        #e = Erds(**self.cookies)
        #e.save()

    def pick(self):
        pass

    def doit(self,action):
        if action == 'save':
            self.save()
        elif action == 'pick':
            return self.pick()

class UiFormDataProcesser(CookiesProcesser):

    data_category = dynamic_conf_category['UIform']

    def __init__(self, ERD_ID, cookies = {}, ERD_model = Erds):
        self.ERD_ID = ERD_ID
        self.cookies = cookies
        self.ERD_model = ERD_model

    def save(self):
        '''
        auto ignore the data outof 'data_category'.
        '''
        save_list = []
        except_list = []
        if not self.cookies:
            print("cookies is empty, do nothing.");return
        for c in self.cookies:
            if c in UiFormDataProcesser.data_category:
                save_list.append(c)
            else:
                except_list.append(c)
        for e in except_list:
            self.cookies.pop(e)

        #e = Erds(**self.cookies)
        #e.save()

    def pick(self):
        pass

    def doit(self,action):
        if action == 'save':
            self.save()
        elif action == 'pick':
            return self.pick()


