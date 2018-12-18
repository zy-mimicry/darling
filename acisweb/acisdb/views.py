from django.shortcuts import render,render_to_response

# Create your views here.
import json

def index(request):
    List = ['memeda', 'abcd']
    Dict = {'site': "www", 'name': 'rex'}
    context = {'List' : json.dumps(List),
               'Dict' : json.dumps(Dict),
    }
    return render_to_response('acisdb/index.html', context)
