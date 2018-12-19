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

def index(request):
    return render(request, 'LigerUI/main.htm', {})

def FT_index(request):
    cookies = [{
        'ERD_ID' : '100',
        'Description': "DDD",
        'HLD': 'HLD link or FileHold ID',
        'Version' : "1.0.0",
        'Age':"date----",
        'Status' : "done",
        'LastModifier':"Rex Zheng",
        'History' : "1.0",
        'hello': 'https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857',
        "fuck" : 'https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857',
        'L2_Ticket':"https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857",
        'JIRA_BUG_Ticket': "https://confluence.sierrawireless.com/display/FWA/2018-12-13+Meeting+Minutes",
        'TestCases': "ACIS_TEST_CASES",
        'TestReports': "ACIS_TEST_REPORT",
        'Platform' : "SD55",
    }]
    return render(request, 'LigerUI/ACIS/FT_table.htm', {'cookies' : json.dumps(cookies)})


# < DEBUG > #
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

    return render(request, 'LigerUI/ACIS/rex_test_page.htm', {'cookies' : json.dumps([FT_TABLE])})


def shw_jump(request):
    cookies = [{
        'ERD_ID' : '100',
        'Description': "DDD",
        'HLD': 'HLD link or FileHold ID',
        'Version' : "1.0.0",
        'Age':"date----",
        'Status' : "done",
        'LastModifier':"Rex Zheng",
        'History' : "1.0",
        'hello': 'https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857',
        "fuck" : 'https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857',
        'L2_Ticket':"https://confluence.sierrawireless.com/pages/viewpage.action?pageId=128096857",
        'JIRA_BUG_Ticket': "https://confluence.sierrawireless.com/display/FWA/2018-12-13+Meeting+Minutes",
        'TestCases': "ACIS_TEST_CASES",
        'TestReports': "ACIS_TEST_REPORT",
        'Platform' : "SD55",
    }]
    return render(request, 'LigerUI/ACIS/shw_test_page.htm', {'cookies' : json.dumps(cookies)})
