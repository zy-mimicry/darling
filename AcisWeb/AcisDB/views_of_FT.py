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
