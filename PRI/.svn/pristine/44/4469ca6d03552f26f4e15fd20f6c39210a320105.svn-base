# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
import time


from apps import PriDbConfig
from django.apps import apps as APPS
import models
import os,re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_DIR=os.path.join(BASE_DIR,'templates')


def oempri_select(request):
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'select_oempri_data.htm')
    return render(request, template)

def fwtools_select(request):
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'select_fwtools_data.htm')
    return render(request, template)
    
def flow_select(request):
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'select_flow_data.htm')
    return render(request, template)

def factory_select(request):
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'select_factory_data.htm')
    return render(request, template)

def test_select(request):
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'test_select_data.htm')
    return render(request, template)
