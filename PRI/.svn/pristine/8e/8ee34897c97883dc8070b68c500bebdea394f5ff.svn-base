# coding = 'utf-8'
from __future__ import unicode_literals
import xlrd
import os
import sys
import argparse
import django
 
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PRI_System.settings")
django.setup()

from PRI_DB.models import *  
reload(sys)  
sys.setdefaultencoding('utf-8')
import jira
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../../lib')))
from myjira import *
import time, datetime
from mycommon import *

def exec_cmd(cmd):
    ret,rpt = my_cmd(cmd,system=True,output=True)
    # print ret
    # print rpt
    return ret,rpt
def exec_svn_update():
    cmd =         'svn up .'
    cmd += '\r\n'+'svn up %s'%os.path.join(pathname, '../../lib')
    ret,rpt = exec_cmd(cmd)
    return ret,rpt
def exec_migrate_PRI_DB():
    cmd =         'python manage.py makemigrations PRI_DB'
    cmd += '\r\n'+'python manage.py migrate PRI_DB'
    ret,rpt = exec_cmd(cmd)
    return ret,rpt
def exec_sync_jira_ticket_to_mysql():
    cmd =         ''
    cmd += '\r\n'+r'@start python PRI_DB\jira_to_mysql.py -all'
    ret,rpt = exec_cmd(cmd)
    return ret,'start task success, please wait until the task is finished!'
def exec_restart_web_server():
    cmd =         ''
    cmd += '\r\n'+'@start PRI_System_start_dbg.bat 5'
    ret,rpt = exec_cmd(cmd)
    return ret,'restart success, please wait until the server is ok!'
def exec_test_web_server():
    cmd =         'ipconfig'
    ret,rpt = exec_cmd(cmd)
    return ret,rpt

if __name__ == "__main__":
    exec_migrate_PRI_DB()