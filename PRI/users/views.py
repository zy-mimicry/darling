# -*- coding1: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_DIR=os.path.join(BASE_DIR,'templates')
# Create your views here.

# def LigerUI(request):
#     return HttpResponse("Hello world ! ")
def LigerUI(request):
    context          = {}
    # context['hello'] = 'Hello World!'
    # print request.path,'->',request.path.replace(r'/LigerUI',r'LigerUI/Source')
    # request_path=request.path.lstrip('/')
    # fullfile_path=os.path.join(templates_DIR,request_path)
    # print request_path
    # # return HttpResponse(my_data, content_type='application / octet - stream')
    # if os.path.exists(fullfile_path):
    #     # return HttpResponseRedirect(request_path)
    #     return render(request, request_path, context)
    # else:
    #     print fullfile_path,'not exist'
    #     return HttpResponse("not exist")
    # return render(request, request.path.replace(r'/LigerUI',r'LigerUI/Source'), context)
    return HttpResponseRedirect(r'LigerUI/main.htm')
