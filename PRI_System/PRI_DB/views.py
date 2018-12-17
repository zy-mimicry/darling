from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

# import os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# templates_DIR=os.path.join(BASE_DIR,'templates')

def index(request):
    return HttpResponseRedirect('LigerUI/main.htm')

    # template = os.path.join(templates_DIR, 'PRI_DB', 'LigerUI','main.htm')
    # context = {}
    #template = loader.get_template('PRI_DB/test_page.htm')
    #template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'test_page.htm')
    #return render(request, 'PRI_DB/LigerUI/main.htm', context)
    #return render(request, template, context)
    #return HttpResponseRedirect('LigerUI/main.htm')
