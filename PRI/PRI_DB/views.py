# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.template import RequestContext
import time
from django.db.models import Q
from django.db.models import Func, F, Value


from apps import PriDbConfig
from django.apps import apps as APPS
from PRI_DB.models import *  
import os,re,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_DIR=os.path.join(BASE_DIR,'templates')
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../lib')))

import mycommon
from mycommon import *
mycommon.__parent__['logpath']=__file__
mycommon.__parent__['loglevel']=logging.DEBUG
__version__ = "1.00"
mycommon.__version__=__version__
import myconst
from myconst import *

# Create your views here.

cfg_dict = {
    'UserName':'',
    'LogUser':True,
}
err_dict = {
    'not_login': 'Operated Failed, Please login in the PRI_System first! <a href="/login/">login</a>',
    'not_permit': 'Operated Failed, You are not permit to do this operation!',
    'no_user_input': 'Operated Failed, No user input for this operation!',
    'login_err': 'username or password is not correct!',
    'login_out': 'login out success!',
    'login_in': 'login in success!',
    'update_succ': 'Update success!',
    'delete_succ': 'Delete success!',
    'sync_succ': 'Sync From Jira success!',
    'comments_str': '<!--',
    'comments_end': '-->',
    'table_empty': 'your visit table is empty!',
    'table_notexist': 'your visit table(%s) is not exist!',
    'template_notexist': 'your visit template(%s) is not exist!',
    'op_empty': 'your operattion is empty!',
    'op_notsupport': 'your operattion(%s) is supported!',
    'table_noid': 'can not find the key id for [%s]!',
    'start_build_succ': 'Start build job success!',
    'stop_build_succ': 'Stop job success!',
    'stop_job_fail': 'This job is not exist!',
    'op_repeat': 'This operation has excuted!',
    'op_fail': 'This job has not build!', 
    'reviewed_end': 'This ticket had reivewed, please ask the administrator to reopen!', 
}

def parsepath(request,def_dict={},tolower=True):
    path=request.get_full_path()
    parastr=re.split(r'[?/]+',path)[-1]
    paradict={}
    for ps in parastr.split('&'):
        pv=ps.split('=')
        if len(pv)==2:paradict[pv[0]]=pv[1]
    req= request.POST if request.POST else request.GET
    paradict.update( dict( req.items() ) )
    for k in def_dict:
        paradict[k] = def_dict[k] if k not in paradict else (paradict[k].lower() if tolower else paradict[k])
    return paradict

def login(request):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'login.html')
    context        = {'err':'','isloginsucc':False,'nowtime':nowtime,'comments_start':'','comments_end':'','username':''}
    REQ = parsepath(request)
    print 'login:',REQ
    # print 'is_authenticated:',request.user.is_authenticated()
    if REQ.has_key('op') and REQ['op']=='logout':
        if 'username' in request.session:
            context['username']=request.session['username']
        username = str(request.user)
        request.session['username'] = ''
        context['err'] = err_dict['login_out']
        auth.logout(request)
        add_operate_log(username, Operate='logout', Result='Y', Description='logout success')
    elif REQ.has_key('username') and REQ.has_key('password'):
        username = REQ['username']
        password = REQ['password']
        context['username'] = username
        # user = auth.authenticate(username = username,password = password)
        user = my_authenticate(username = username,password = password)
        if user is not None and user.is_active:
            auth.login(request,user)
            context['isloginsucc']=True
            request.session['username'] = username
            add_operate_log(username, Operate='login', Result='Y', Description='login success')
        else:
            context['err'] = err_dict['login_err']
            request.session['username'] = ''
            auth.logout(request)
            add_operate_log(username, Operate='login', Result='N', Description='login failed')
    elif pri_is_authenticated(request):
        context['isloginsucc'] = True
        context['username'] = str(request.user)
    if context['isloginsucc']:
        context['comments_start'] = err_dict['comments_str']
        context['comments_end'] = err_dict['comments_end']
        context['err'] = '[%s] %s'%(context['username'],err_dict['login_in'])

    return render(request, template, context)
    # return render_to_response(template, RequestContext(request,context))

def pri_is_inGroup(request,group='admins'):
    return group in get_user_group(request.user)

def pri_is_authenticated(request):
    return request.user.is_authenticated()

def pri_db_operation(request):
    context        = {'err':'','rlt':'','id':'-1','template':'','fmt':'','issucc':'1'}
    REQ = {'tb':'','op':'query','fmt':'','ext':''}
    REQ = parsepath(request,REQ)
    if 0:
        print 'REQ:',REQ

    if not REQ['tb']:
        context['err'] = err_dict['table_empty']
        return HttpResponse(context['err'], status=404)
    elif not is_valid_table(REQ['tb']):
        context['err'] = err_dict['table_notexist']%(REQ['tb'])
        return HttpResponse(context['err'], status=404)

    cfg_dict['UserName'] = str(request.user)
    tbobj = APPS.get_model(PriDbConfig.name, REQ['tb'])
    if REQ['op']=='list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'oempri_list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'fwtools_list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'factory_list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'flow_list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op']=='list1':#REQ['ext'] will work
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'query':
        result = table_query(request, tbobj, REQ, context)
    elif REQ['op']=='update':
        result=table_update(request,tbobj,REQ,context)
    elif REQ['op']=='updatepca':
        result=table_update_pca(request,tbobj,REQ,context)
    elif REQ['op'] == 'update1':#REQ['ext'] will work,and append REQ['Description']
        gen_description(request,tbobj,REQ)
        result = table_update(request, tbobj, REQ, context)
    elif REQ['op'] == 'update_reg':#REQ['ext'] will work,and append REQ['Description']
        gen_description(request,tbobj,REQ)
        result = table_update_reg(request, tbobj, REQ, context)
    elif 'editfield' in REQ['op'] or REQ['op'] == 'delete':
        result = table_editfield(request, tbobj, REQ, context)
    elif REQ['op'] == 'batchupdate':
        result = table_batch_update(request, tbobj, REQ, context)
    elif 'syncfromjira' in REQ['op']:
        result = table_syncfromJira(request, tbobj, REQ, context)
    elif REQ['op'] == 'req-view':
        result=table_view_req(request, tbobj, REQ, context)
    elif 'req-' in REQ['op'] :
        result = table_req(request, tbobj, REQ, context,ext='_init')
    else:
        # REQ['op'] not in ['init','list','list1','query','update','batchupdate','insert','delete']:
        context['err'] = err_dict['op_notsupport']%(REQ['op'])
        return HttpResponse(context['err'], status=404)

    if REQ['fmt'].lower()=='json':
        return HttpResponse(json.dumps(context['rlt'], ensure_ascii=False))
    elif not os.path.exists(context['template']):
        context['err'] = err_dict['template_notexist']%(context['template'])
        return HttpResponse(context['err'], status=404)
    else:
        return render(request, context['template'], context)

def table_editfield(request,tbobj,REQ,context,ext=''):
    qti_data = []
    qti_err = []
    ids = REQ['id'].strip(',').split(',')
    context['op'] = REQ['op']
    context['id'] = ','.join(ids)
    context['fieldname']='' if 'fieldname' not in REQ else  REQ['fieldname']
    context['fieldvalue']='' if 'fieldvalue' not in REQ else  REQ['fieldvalue']
    context['fieldtype']='' if 'fieldtype' not in REQ else  REQ['fieldtype']
    context['tb']='' if 'tb' not in REQ else  REQ['tb']
    context['issucc'] = '0'
    if REQ['op']=='delete':
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        elif not pri_is_inGroup(request, 'admins'):
            context['err'] = err_dict['not_permit']
            context['issucc'] = '0'
        else:
            # context['issucc'] = '1'
            context['err'] = err_dict['delete_succ']
            for id in ids:
                qdict = {'Key':id} if '-' in id.strip('-') else {'id': id}
                delete_data(request,tbobj, qdict)

    else:
        if context['fieldname'] and context['fieldvalue']:
            if not pri_is_authenticated(request):
                context['err'] = err_dict['not_login']
                context['issucc'] = '0'
            elif not pri_is_inGroup(request, 'admins'):
                context['err'] = err_dict['not_permit']
                context['issucc'] = '0'
            elif REQ['op']=='editfield':
                if REQ['ext']=='close': context['issucc'] = '1'
                context['err'] = err_dict['update_succ']
                if context['fieldvalue'].lower()=='none':context['fieldvalue']=''
                for id in ids:
                    qdict = {'Key':id} if '-' in id else {'id': id}
                    ndict = {context['fieldname']: context['fieldvalue']}
                    update_data(request,tbobj, qdict, ndict)
        context['op']='editfield'


    context['template'] = table_get_template(REQ, ext='editfield')
    # context['template'] = os.path.join(templates_DIR, 'LigerUI', 'PRI', '%s%s_table.htm' % (REQ['tb'],ext))
    context['Description'] = '\n'.join(qti_err)
    fieldnames=[]
    var_fieldnames=[]
    var_fieldtypes=[]
    for f in tbobj._meta.fields:
        fieldnames.append('<option value="%s">%s</option>'%(f.name,f.name))
        var_fieldnames.append(f.name)
        help_text=f.help_text
        if not help_text:help_text=str(type(f))
        var_fieldtypes.append(help_text)
    # fieldnames = ['<option value="%s">%s</option>'%(f.name,f.name) for f in tbobj._meta.fields]
    context['fieldnames'] = ''.join(fieldnames)
    context['var_fieldnames'] = ';'.join(var_fieldnames)
    context['var_fieldtypes'] = ';'.join(var_fieldtypes)
    tablelist = ''.join(['<option value="%s">%s</option>'%(f,f) for f in get_tables()])
    context['tablelist'] = tablelist

    return 0,''

def table_syncfromJira(request,tbobj,REQ,context,ext=''):
    qti_data = []
    qti_err = []
    ids = REQ['id'].strip(',').split(',')
    context['op'] = REQ['op']
    context['id'] = ','.join(ids)
    context['tb']='' if 'tb' not in REQ else  REQ['tb']
    context['issucc'] = '0'
    if 'syncfromjira' in REQ['op']:
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        elif not pri_is_inGroup(request, 'admins'):
            context['err'] = err_dict['not_permit']
            context['issucc'] = '0'
        else:
            # context['issucc'] = '1'
            context['err'] = err_dict['sync_succ']
            tickets=table_get_field(tbobj,'Key',ids)
            filter=' or '.join(['key=%s'%t for t in tickets])
            import jira_to_mysql
            if 'QTI' in filter:
                jira_to_mysql.qti_to_mysql(filter,tbobj)
            elif 'week' in REQ['op']:
                jira_to_mysql.oempriweek_to_mysql(filter, tbobj)
            elif 'flow' in REQ['op']:
                jira_to_mysql.flow_jira_to_mysql(filter, tbobj)
            elif 'factory' in REQ['op']:
                jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            elif 'assignticket' in REQ['op']:
                if 'username' not in REQ:
                    context['err'] = err_dict['no_user_input']
                    context['issucc'] = '0'
                else:
                    jira_to_mysql.jira_assign_tickets(tickets, REQ['username'] )
                    jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            elif 'createfacttask' in REQ['op']:
                jira_to_mysql.jira_create_fact_subtask(tickets, str(request.user))
                jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            elif 'approve-AllFilesAdded'.lower() in REQ['op']:
                jira_to_mysql.jira_close_fact_subtasks(tickets, 'AllFilesAdded')
                jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            elif 'approve-SpkgValidated'.lower() in REQ['op']:
                jira_to_mysql.jira_close_fact_subtasks(tickets, 'SpkgValidated')
                jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            elif 'approve-LogValidated'.lower() in REQ['op']:
                jira_to_mysql.jira_close_fact_subtasks(tickets, 'LogValidated')
                jira_to_mysql.factory_jira_to_mysql(filter, tbobj)
            else:
                jira_to_mysql.jira_to_mysql(filter, tbobj)
            context['err']=filter+' '+context['err']
    else:
        context['issucc'] = '0'
        context['err'] = err_dict['op_notsupport']

    context['template'] = table_get_template(REQ, ext='syncfromjira')
    context['Description'] = '\n'.join(qti_err)

    return 0,''


def table_req(request,tbobj,REQ,context,ext=''):#req-chk,req-add,req-rmv
    #get/gen ReviewID
    #get all ReviewID
    #get all qti
    qti_data = []
    qti_err = []
    Product = '' if 'Product' not in REQ else REQ['Product']
    ReviewID = ('' if REQ['op'] == 'req-rmv' else mytimex()) if 'ReviewID' not in REQ else REQ['ReviewID']
    if Product and '-' not in ReviewID:ReviewID='%s-%s'%(Product,ReviewID)
    ids = REQ['id'].strip(',').split(',')
    #
    context['Product'] = Product
    context['op'] = REQ['op']
    context['id'] = ','.join(ids)

    if REQ['op'] == 'req-add':
        #get all sku
        sku_rows=table_get_skux(Product)
        #add qti with sku to checkin_list
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        else:
            qit_result = table_add_qti_to_req(request,ReviewID, ids, sku_rows, qti_err)
    elif REQ['op'] == 'req-rmv' and '-' in ReviewID:
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        else:
            qit_result = table_rmv_qti_from_req(request,ReviewID,ids,qti_err)
        ReviewID=mytimex()
    else:#if REQ['op']=='req-chk':
        # check qti is ready
        qit_result = table_is_qti_ready(request,ReviewID, ids, qti_data, qti_err)
        if qti_data and '9x40' in qti_data[0].Key.lower():context['Product']='AR759x'
        if not REQ['op'] == 'req-rmv' and qit_result:context['op'] = 'req-add'

    context['template'] = table_get_template(REQ, ext='%s_table'%ext)
    # context['template'] = os.path.join(templates_DIR, 'LigerUI', 'PRI', '%s%s_table.htm' % (REQ['tb'],ext))
    context['Description'] = '\n'.join(qti_err)
    context['ReviewID'] = ReviewID
    ReviewIDs = table_get_reviewid()
    context['ReviewIDs'] = gen_options(ReviewIDs,ReviewID)

    #update qti ReviewStatus=Reviewing and ReviewID
    #calc which sku to suggest
    #add new record to CHECKIN_List
    return 0,''

def gen_options(items,sel):
    if sel and sel not in items:items.insert(0, sel)
    for i in range(len(items)):
        items[i]='<option %s>%s</option>'%('selected'if items[i]==sel else '',items[i])
    return ''.join(items)

def table_test():
    # qti_err = []
    # qti_data = []
    # ids = [11,17]
    # ReviewID=''
    # print table_is_qti_ready(ReviewID,ids,qti_data,qti_err)
    # print qti_data
    # print qti_err
    # print table_get_modelx()[0]
    # print table_get_skux('ar758x')
    pass

def my_authenticate(username,password=''):
    ldap_serv = 'ldap://cnszx-dc01.sierrawireless.local' #nslookup
    ldap_serv = 'ldap://cnshz-nv-dc01.sierrawireless.local' #nslookup
    domain = 'sierrawireless'
    baseDN = 'OU=USERS,OU=ACCOUNTS,OU=SWI,DC=sierrawireless,DC=local'
    ldap_result = 0
    ldap_u_dict = {}
    try:
        import ldap
        conn = ldap.initialize(ldap_serv)
        conn.simple_bind_s(username + "@" + domain, password)
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = '(|(sAMAccountName='+username+'))'
        ldap_result_id = conn.search(baseDN, searchScope, searchFilter, None)
        result_type, result_data = conn.result(ldap_result_id, 1)
        if result_data:ldap_u_dict=result_data[0][1]
        ldap_result = 1
    except ldap.LDAPError,err:
        ldap_result=0
        ldap_error = 'Error: Connect to %s failed, %s.' % (ldap_serv, err.message['desc'])
        print ldap_error
    
    if ldap_result:
        if not User.objects.filter(username=username).count():
            User.objects.create(username=username)
        if ldap_u_dict:
            first_name,last_name=ldap_u_dict['displayName'][0].split(' ')
            email=ldap_u_dict['mail'][0]
            # print first_name,last_name,email
            User.objects.filter(username=username).update(first_name=first_name,last_name=last_name,email=email)
        from django.contrib.auth import get_user_model
        UserModel=get_user_model()
        user = UserModel._default_manager.get_by_natural_key(username)
    else:
        # password='config_12345'
        # user=User.objects.get(username=username)
        # user.set_password(password)
        # user.save()
        user = auth.authenticate(username=username, password=password)
    return user

def get_user_group(user):
    grps = Group.objects.filter(user=user)
    return [ grp.name for grp in grps]

def table_rmv_qti_from_req(request,ReviewID,ids,qti_err):
    ret_result=True
    for id in ids:
        qit_rlt = True
        if QTI_List.objects.filter(id=id).exists():
            qti_row = QTI_List.objects.filter(id=id).all()[0]
            # update qti ReviewStatus=Reviewing and ReviewID
            qdict = {'id': id}
            ndict = {'ReviewStatus':'','ReviewID': ''}
            update_data(request,QTI_List, qdict, ndict)
            qdict = {'ReviewID': ReviewID,'Key':qti_row.Key}
            qti_err.append('OK: remove CHECKIN_List with %s' % (qdict))
            delete_data(request,CHECKIN_List,qdict)
        else:
            qti_err.append('ERR: %s not exist'%id)
            qit_rlt = False

        #delete not use ReviewID
        qdict = {'ReviewID': ReviewID}
        if not CHECKIN_List.objects.filter(**qdict).exists():
            delete_data(request,ReviewID_List, qdict)

        if not qit_rlt:
            ret_result=False
            continue
    return ret_result

def table_add_qti_to_req(request,ReviewID,ids,sku_data,qti_err):
    ret_result=True
    for id in ids:
        qit_rlt = True
        if QTI_List.objects.filter(id=id).exists():
            # add new record to ReviewID_List
            ndict = {'ReviewID': ReviewID}
            update_data(request,ReviewID_List, ndict, ndict)

            qti_row = QTI_List.objects.filter(id=id).all()[0]
            # update qti ReviewStatus=Reviewing and ReviewID
            qdict = {'id': id}
            ndict = {'ReviewStatus':'Reviewing','ReviewID': ReviewID}
            # print qdict,ndict
            update_data(request,QTI_List, qdict, ndict)
            UserName=cfg_dict['UserName']
            #log data to history
            desc='add CHECKIN_List: with %s'%({'ReviewID': ReviewID,'Key':qti_row.Key})
            # print desc
            add_operate_log(str(request.user), Operate='add', Result='Y', Description=desc)
            LogUser_Off(True) #------------too many data so to close the log
            sku_index=0
            for sku_obj in sku_data:
                # calc which sku to suggest
                sku_index+=1
                Suggest=calc_suggest(sku_obj,qti_row)#'N'
                # add new record to CHECKIN_List
                qdict = {'ReviewID': ReviewID,'Key':qti_row.Key,'SKU':sku_obj.SKU,'CarrierPN':sku_obj.CarrierPN}
                ndict = {'ReviewID': ReviewID,'Key':qti_row.Key,'SKU':sku_obj.SKU,'CarrierPN':sku_obj.CarrierPN,
                        'SWIPrjName':sku_obj.SWIPrjName,'Product':sku_obj.Product,'Customer':sku_obj.Customer,'Category':sku_obj.Category,
                         # 'Apply':'N',
                         'Suggest':Suggest,
                         'Description':'%s %s add'%(mytime(),UserName),
                         'UserName':UserName}
                desc = 'OK: add %s to %s with %s' % (qti_row.Key,sku_obj.SKU,ReviewID)
                curop= 'update' if CHECKIN_List.objects.filter(**qdict) else 'add'
                qti_err.append('OK: %s %s to %s with %s' % (curop,qti_row.Key,sku_obj.SKU,ReviewID))
                # print sku_index,qdict,ndict
                update_data(request,CHECKIN_List, qdict, ndict)
            LogUser_On(True)
        else:
            qti_err.append('ERR: %s not exist'%id)
            qit_rlt = False
        if not qit_rlt:
            ret_result=False
            continue
    return ret_result

def calc_suggest(sku_obj,qti_row):
    Suggest='N'
    SKU=sku_obj.SKU
    Category=sku_obj.Category.lower()
    Customer=sku_obj.Customer.lower()
    Product=sku_obj.Product.lower()
    CarrierPN=sku_obj.CarrierPN.replace('T-Mobile','TMO').lower()

    CarrierCustomer = '' if not qti_row.CarrierCustomer else qti_row.CarrierCustomer.lower()
    ticketid = qti_row.Key

    if CarrierCustomer=='all':
        if Category=='commercial':Suggest='Y'
    elif Customer in CarrierCustomer:Suggest='Y'
    elif Product in CarrierCustomer:Suggest='Y'
    elif CarrierCustomer:
        carrs = re.findall('_([a-z\-]+)',CarrierPN)
        for carr in carrs:
            if carr in CarrierCustomer:
                Suggest = 'Y'
                break
    # mylog('ticketid=%s,Suggest=%s,SKU=%s,Category=%s,Customer=%s,Product=%s,CarrierPN=%s, CarrierCustomer=%s'%(ticketid,Suggest,SKU,Category,Customer,Product,CarrierPN,CarrierCustomer))
    return Suggest

def table_is_qti_ready(request,ReviewID,ids,qti_data,qti_err):
    ret_result=True
    ready_status = 'Assigned/In Review/Checked In'.split('/')
    for id in ids:
        qit_rlt = True
        if QTI_List.objects.filter(id=id).exists():
            qti_row = QTI_List.objects.filter(id=id).all()[0]
            qti_key = '%s[%s]'%(qti_row.Key,qti_row.id)
            # check ticket in correct status:Assigned/In Review/Checked In
            if not qti_row.Status or qti_row.Status not in ready_status:
                qti_err.append('ERR: %s status(%s) is not ready(Assigned)' %( qti_key, qti_row.Status))
                qit_rlt = False
            # check ticket not checkined:(ReviewStatus and ReviewID are empty)
            elif qti_row.ReviewStatus and qti_row.ReviewID==ReviewID:
                qti_err.append('OK: %s status(%s) is ready(reviewing)' % (qti_key, qti_row.Status))
            elif qti_row.ReviewStatus:
                qti_err.append('ERR: %s ReviewStatus(%s:%s) is in reiewed' %( qti_key, qti_row.ReviewStatus,qti_row.ReviewID))
                qit_rlt = False
            elif qti_row.ReviewID:
                qti_err.append('ERR: %s ReviewID(%s) is in reiewed' %( qti_key, qti_row.ReviewID))
                qit_rlt = False
            else:
                qti_err.append('OK: %s status(%s) is ready' % (qti_key, qti_row.Status))
        else:
            qti_err.append('ERR: %s not exist'%id)
            qit_rlt = False
        if not qit_rlt:
            ret_result=False
            continue
        qti_data.append(qti_row)
    return ret_result
def is_carrier_pn_match(skupn,checkinpn,minsize=2):
    skupns=re.findall('(\d+)_',skupn)
    checkinpns=re.findall('(\d+)_',checkinpn)
    return set(skupns)==set(checkinpns) and len(skupns)>=minsize
def table_view_req(request, tbobj, REQ, context):

    if REQ['tb'].lower()=='checkin_list':
        context['project_list_all'] = ';'.join(table_get_project('AR'))
        context['project_list_9x28'] = ';'.join(table_get_project('AR758X'))
        context['project_list_9x40'] = ';'.join(table_get_project('AR759X'))
    ret_result=True
    ret_dict={}
    ret_data=[]
    ReviewIDs=table_get_reviewid()
    ReviewID = ReviewIDs[0] if 'ReviewID' not in REQ else REQ['ReviewID']
    context['ReviewID']=ReviewID
    Product=ReviewID.split('-')[0]
    checkin_rows = CHECKIN_List.objects.filter(ReviewID=ReviewID).order_by('Key')
    #sku_rows = table_get_skux(Product)
    # order_lst,sortnames,sortorders=[],REQ['sortname'].split(','),REQ['sortorder'].split(',')
    sortorder='asc' if 'sortorder' not in REQ else REQ['sortorder']
    sortname= '' if 'sortname' not in REQ else REQ['sortname']
    if sortname: 
        order_str = sortname if sortorder=='asc' else '-%s'%sortname
    else:
        order_str=''
    sku_rows = table_get_skux_from_checkin_list(order_str,ReviewID,checkin_rows[0].Key,Product,project= '' if 'SWIPrjName' not in REQ else REQ['SWIPrjName'].replace('NULL',''))
    if not sku_rows:
        sku_rows = table_get_skux(Product,project= '' if 'SWIPrjName' not in REQ else REQ['SWIPrjName'].replace('NULL',''))
    #print 'sku_rows:',len(sku_rows)
    #print 'checkin_rows:',len(checkin_rows)
    key_fields='id,SWIPrjName,SKU,Product,Customer,CarrierPN,Category'.split(',')
    key_titles=[]
    for sku_row in sku_rows:
        view_dict={}
        is_reviewing=False
        for f in key_fields:
            # view_dict[f]=getattr(sku_row,f)
            view_dict[f] = str(getattr(sku_row, f)).strip('"')
        for checkin_row in checkin_rows:
            valid_sku=is_valid_sku(checkin_row.SKU)
            #if (checkin_row.SKU and checkin_row.SKU==view_dict['SKU']) and is_carrier_pn_match(checkin_row.CarrierPN,view_dict['CarrierPN']):
            if (valid_sku and checkin_row.SKU==view_dict['SKU']) or (not valid_sku and checkin_row.CarrierPN.strip('"')==view_dict['CarrierPN']):
                is_reviewing=True
                id=checkin_row.id
                Key=checkin_row.Key
                Apply=checkin_row.Apply
                Suggest=checkin_row.Suggest
                Status=checkin_row.Status
                Description=checkin_row.Description
                update_cnt=len(re.split(r'[\r\n]+',Description))
                view_dict[Key] = '%s%s-%s-%s-%s'%(Apply,Suggest,id,update_cnt,Status)
                if not Key=='-1' and Key not in key_titles:key_titles.append(Key)
        if is_reviewing:
            ret_data.append(view_dict)
    columns=["{ display: '%s', name: '%s', width: 95, align: 'center', render: qti_callback, }"%(qti,qti) for qti in key_titles]
    context['columns']=',\n                '.join(columns)
    context['ReviewIDs'] = gen_options(ReviewIDs,ReviewID)
    context['template'] = table_get_template(REQ,ext='_view')
    context['rlt']={'Rows':ret_data,'Total':len(ret_data)}
    return 0,''

def table_get_field(tobj,field,ids):
    data = [item[0] for item in tobj.objects.filter(id__in =ids).values_list(field)]
    return data

def table_get_reviewid():
    data = [item[0] for item in ReviewID_List.objects.values_list('ReviewID').order_by('-id').distinct()]
    return data

def table_get_sku():
    data = [item['SKU'] for item in SKU_List.objects.values('SKU').distinct()]
    return data

def table_get_skux(Product,Category='Commercial|Lab',project=''):#AR758x/AR759x
    # from django.db.models import Q
    # User.objects.filter(Q(state=0) | Q(state=1))
    if 'AR758' in Product:Product+='|AR858x'
    Product=Product.replace('X','').replace('x','')
    myfilter={'Product__iregex':Product,'Category__iregex':Category}
    if project:myfilter['SWIPrjName__in']=project.split(';')
    SKU_List.objects.filter(SWIPrjName__isnull=True).update(SWIPrjName='')
    data= SKU_List.objects.filter(**myfilter)
    # print 'myfilter:',len(data),myfilter
    return data

def table_get_skux_from_checkin_list(order_str,ReviewID,Key,Product,Category='Commercial|Lab',project=''):#AR758x/AR759x
    # from django.db.models import Q
    # User.objects.filter(Q(state=0) | Q(state=1))
    if 'AR758' in Product:Product+='|AR858x'
    Product=Product.replace('X','').replace('x','')
    myfilter={'ReviewID':ReviewID,'Key':Key,'Product__iregex':Product,'Category__iregex':Category}
    if project:myfilter['SWIPrjName__in']=project.split(';')
    CHECKIN_List.objects.filter(SWIPrjName__isnull=True).update(SWIPrjName='')
    data= CHECKIN_List.objects.filter(**myfilter)
    var_fieldnames=[f.name for f in CHECKIN_List._meta.fields]
    if order_str and order_str.strip('-') in var_fieldnames:data=data.order_by(order_str)
    # print 'myfilter:',len(data),myfilter
    return data

def table_get_model(Product=''):
    if 'AR758' in Product:Product+='|AR858x'
    Product=Product.replace('X','').replace('x','')
    data = [item[0].upper() for item in SKU_List.objects.filter(Product__iregex=Product).values_list('Product').distinct()]
    return data

def table_get_customer(Product=''):
    if 'AR758' in Product:Product+='|AR858x'
    Product=Product.replace('X','').replace('x','')
    data = [item[0] for item in SKU_List.objects.filter(Product__iregex=Product).values_list('Customer').distinct()]
    return data

def table_get_project(Product=''):
    if 'AR758' in Product:Product+='|AR858x'
    Product=Product.replace('X','').replace('x','')
    data = [item[0] for item in SKU_List.objects.filter(Q(Product__iregex=Product),~Q(SWIPrjName= '')).values_list('SWIPrjName').distinct()]
    return data

def table_get_component():
    data = [item[0] for item in Jira_List.objects.values_list('Components').distinct()]
    return data

def table_get_reporter():
    data = [item[0] for item in Jira_List.objects.values_list('Reporter').distinct()]
    return data

def table_get_Status(tp='OEMPRI'):
    data = {
        'FWTOOLS':table_get_sys_config('fwtools_status',','.join(['None','done','Closed','Integrated','Checked In','In Review','Assigned','CCB','Analysis','New','To Do','In Progress'])).split(','),
        'OEMPRI': table_get_sys_config('oempri_status',','.join(['None','Closed','Validated','Integrated','Reviewed','Tested','Generated','In Progress','Open'])).split(','),
        'QTI':    table_get_sys_config('fwtools_status',','.join(['None','done','Closed','Integrated','Checked In','In Review','Assigned','CCB','Analysis','New','To Do','In Progress'])).split(','),
    }
    return data[tp]

def table_set_sys_config(Name,Value,Group='User'):
    filter={'Name':Name}
    cdict={'Name':Name,'Value':Value,'Group':Group}
    userinfo=User.objects.filter(username=Name.split('_')[0]).values('first_name','last_name')
    if userinfo:
        cdict['Owner']='%s %s'%(userinfo[0]['first_name'],userinfo[0]['last_name'])
    if Sys_Config.objects.filter(**filter).exists():
        Sys_Config.objects.filter(**filter).update(**cdict)
        # print '    exist:',filter,cdict
    else:
        p=Sys_Config.objects.create(**cdict)
        # print 'not exist:',filter,cdict
        
def table_get_sys_config(Name,default='',Group=''):
    filter={'Name':Name}
    if Group:filter['Group']=Group
    data = Sys_Config.objects.filter(**filter).values_list('Value').distinct()
    if data:return data[0][0]
    return default
def table_get_sys_config_status(Name,default='',Group=''):
    filter={'Name':Name}
    if Group:filter['Group']=Group
    data = Sys_Config.objects.filter(**filter).values_list('Status').distinct()
    if data:return data[0][0]
    return default
    
def table_get_modelx():
    datax = []
    data = table_get_model()
    for item in data:
        if 'AR758' in item: item='AR758x'
        elif 'AR858' in item: item = 'AR758x'
        elif 'AR759' in item: item = 'AR759x'
        if item not in datax:datax.append(item)
    return data,datax

def table_get_template(REQ,ext=''):
    if 'tb' not in REQ:REQ['tb']=''
    if 'ext' not in REQ:REQ['ext']=''
    # tablename[_userext][_myext].htm: SKU_List.htm/CHECKIN_List_view.htm
    if ext=='batch' or REQ['ext']=='batch':htmlname='%s_table.htm' % 'batch'
    elif ext=='delete' or REQ['ext']=='delete':htmlname='%s_table.htm' % 'editfield'
    elif ext=='editfield' or REQ['ext']=='editfield':htmlname='%s_table.htm' % 'editfield'
    elif ext=='syncfromjira' or REQ['ext']=='syncfromjira':htmlname='%s_table.htm' % 'close'
    elif ext=='close' or REQ['ext']=='close':htmlname='%s_table.htm' % 'close'
    else:htmlname='%s%s%s.htm' % (REQ['tb'],REQ['ext'],ext)
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', htmlname)
    return template

def table_list(request,tbobj,REQ,context,ext=''):
    context['template'] = table_get_template(REQ,ext='')
    context['fwtools_statuslist']=';'.join(table_get_Status('FWTOOLS'))
    context['oempri_statuslist']=';'.join(table_get_Status('OEMPRI'))
    context['issuetype_list']=table_get_sys_config('issuetype_list','')
    context['jira_assignees']=table_get_sys_config('jira_assignees','Stone Li')
    context['yellow_assignees']=table_get_sys_config('yellow_assignees','Stone Li,Lares Yang,Bing Huang,Mary Shan')
    if REQ['tb'].lower()=='qti_list':
        context['cus_list_9x28'] = ';'.join(table_get_customer('AR758X'))
        context['pro_list_9x28'] = ';'.join(table_get_model('AR758X'))
        context['cus_list_9x40'] = ';'.join(table_get_customer('AR759X'))
        context['pro_list_9x40'] = ';'.join(table_get_model('AR759X'))
        
    if 'view' in REQ:
        context['view']=REQ['view']
        if 'view_cols' in REQ and REQ['view_cols'] and 'Anonymous' not in str(request.user):
            table_set_sys_config('%s_%s'%(str(request.user),context['view']),REQ['view_cols'],'User')
        for tempview in 'week_view,flow_view,factory_view,fwtools_view,full_view'.split(','):
            context[tempview]=table_get_sys_config('%s_%s'%(str(request.user),tempview))
            # print tempview,context[tempview]
        
    context['rlt'] = filter_2_json_page(tbobj, REQ)
    return 0,''

def table_query(request,tbobj,REQ,context,ext=''):
    context['template'] = table_get_template(REQ,ext='_table')
    if 'id' not in REQ and 'Key' not in REQ:
        context['err'] = err_dict['table_noid'] % (REQ['tb'])
        return HttpResponse(context['err'], status=404)
    else:
        if 'Key' in REQ and not REQ['Key']=='-1':
            qdict={'Key':REQ['Key']}
        else:
            qdict = {'id': REQ['id']}
        rowtext={}
        for rowobj in tbobj.objects.filter(**qdict):
            rowtext = rowobj_2_json(rowobj, tbobj._meta.fields, todict=True)
    if 'Key' in rowtext and 'QTI' in rowtext['Key']:
        if '9X28' in rowtext['Key']:
            cus_list = table_get_customer('AR758X')
            pro_list = table_get_model('AR758X')
        elif '9X40' in rowtext['Key']:
            cus_list = table_get_customer('AR759X')
            pro_list = table_get_model('AR759X')
        else:
            cus_list=pro_list=[]
        context['cus_list']=';'.join(cus_list)
        context['pro_list']=';'.join(pro_list)

    print 'query rowtext:', rowtext
    context.update(rowtext)
    context['rltdisp'] = 'none'
    context['rlt'] = rowtext
    return 0,''

def table_update(request,tbobj,REQ,context):
    context['template'] = table_get_template(REQ,ext='_table')
    rowtext = {}
    for f in tbobj._meta.fields:
        if f.name in REQ:
            if not REQ[f.name] and 'DateTimeField' in str(type(f)): continue
            rowtext[f.name] = REQ[f.name]
    print 'update rowtext:', rowtext
    if 'id' not in REQ:
        context['err'] = err_dict['table_noid'] % (REQ['tb'])
        context['issucc'] = '0'
    else:
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        else:
            for xid in rowtext['id'].strip(',').split(','):
                rowtext['id']=xid
                update_data(request,tbobj, {'id': xid}, rowtext)
    context.update(rowtext)
    context['rltdisp'] = 'none'
    context['rlt'] = rowtext
    return 0,''

def table_update_reg(request,tbobj,REQ,context):
    context['template'] = table_get_template(REQ,ext='_table')
    rowtext = {}
    for f in tbobj._meta.fields:
        if f.name in REQ:
            if not REQ[f.name] and 'DateTimeField' in str(type(f)): continue
            rowtext[f.name] = REQ[f.name]
    print 'update rowtext:', rowtext
    if 'id' not in REQ:
        context['err'] = err_dict['table_noid'] % (REQ['tb'])
        context['issucc'] = '0'
    else:
        ticketdata=tbobj.objects.filter(id=rowtext['id']).values_list('Key')
        if ticketdata and QTI_List.objects.filter(Key=ticketdata[0][0],ReviewStatus__in=['Done','Reviewed']).all():
            context['err'] = err_dict['reviewed_end']
            context['issucc'] = '0'
        elif not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
        else:
            update_data(request,tbobj, {'id': rowtext['id']}, rowtext)
    context.update(rowtext)
    context['rltdisp'] = 'none'
    context['rlt'] = rowtext
    return 0,''

    
def table_update_pca(request,tbobj,REQ,context):
    context['template'] = table_get_template(REQ,ext='_table')
    rowtext = {}
    for f in tbobj._meta.fields:
        if f.name in REQ:
            if not REQ[f.name] and 'DateTimeField' in str(type(f)): continue
            rowtext[f.name] = REQ[f.name]
    print 'update rowtext:', rowtext
    if 'FSN' not in REQ:
        context['err'] = err_dict['table_noid'] % (REQ['tb'])
        context['issucc'] = '0'
    else:
        update_data(request,tbobj, {'FSN': rowtext['FSN']}, rowtext,isforce=True,islog=False)
    context.update(rowtext)
    context['rltdisp'] = 'none'
    context['rlt'] = rowtext
    return 0,''

def table_batch_update(request,tbobj,REQ,context):
    if REQ['op'] == 'batchupdate':
        context['template'] = table_get_template(REQ, ext='batch')
    else:
        context['template'] = table_get_template(REQ, ext='_table')
    for f in tbobj._meta.fields:
        if f.name not in REQ:
            context[f.name] = ''
        else:
            context[f.name] = REQ[f.name]
    context['rltdisp'] = 'none'
    context['tb'] = REQ['tb']
    if not REQ['op'] == 'init':
        context['rltdisp'] = 'block'
        for f in REQ:
            context['rlt'] += '%s=%s\n' % (f, REQ[f])
    if 'Description' in REQ:
        desc = REQ['Description']
        context['Description'] = desc
        lines = csvtxt2rowcol(desc)
        if not pri_is_authenticated(request):
            context['err'] = err_dict['not_login']
            context['issucc'] = '0'
            rlttxt = []
        else:
            rlttxt = rowcol2dict(request,lines, isstr=True, tbobj=tbobj, addfucn=add_new_data)
        context['rlt'] = '\n'.join(rlttxt)
    return 0,''

# fmd={'a__gte':1,'b__lte':1,'c__in':[1,2,3],'d__ls':2,'e__range':[1,100],'f__lte':1,'g__gtr':1,'h__in':[1,2,3,4,5],'i__lte':1,'J__gtr':2}
# fml='((a & b) or (c) or (d)) & ((e & (f | g)) or (h)) or (i and J)'
def calc_Q_express(fml,fmd):
    q_dict={}
    e=''
    icount=0
    maxcount=1000
    if 1:
        fs=[]
        for s in fml.split():
            if s.lower()=='or' or s=='||':s='|'
            elif s.lower()=='and' or s=='&&':s='&'
            fs.append(s)
        fml= ' '.join(fs)
    while fml:
        exprs=re.findall(r'(\(?([^\(\)]+)\)?)',fml)
        # print fml,'1---------------'
        for expr in exprs:
            expr0,expr1=expr[0].strip(),expr[1].strip()
            if expr1 in ['&','|']:continue
            if expr0[0] in ['&','|']:expr0,expr1=expr0[1:].strip(),expr1[1:].strip()
            if expr0[-1] in ['&','|']:expr0,expr1=expr0[:-1].strip(),expr1[:-1].strip()
            e=expr1.replace(' ','_')
            ks=expr1.strip('() ').split()
            icount+=1
            # print expr,len(ks)
            # print fml,'2-------------',e
            if '(' in expr0 and ')' in expr0:
                fml=fml.replace(expr0,' %s '%e)
            elif len(ks)>2:
                fml=fml.replace(expr0,e)
            else:
                continue
            # print fml,'====---------'
            if e not in q_dict:q_dict[e]=None
            # print 'expr0=[%s][%s][%s]'%(expr[0],expr[1],e),'==len==',len(ks)
            logic='&'
            for k in ks:
                if k.lower() in ['&','|']:
                    logic=k
                    continue
                if k in q_dict and q_dict[k]:
                    tempQ=q_dict[k]
                else:
                    tempQ=None
                    for key in fmd:
                        if k==key.split('_')[0]:
                            if str(fmd[key])[0]=='!':
                                tempQ=~Q(**{key:fmd[key][1:]})
                            else:
                                tempQ=Q(**{key:fmd[key]})
                            break
                if tempQ:
                    if not q_dict[e] or e==k:
                        q_dict[e]= tempQ
                    elif '|' in logic:
                        q_dict[e]= q_dict[e] | tempQ
                    else:
                        q_dict[e]= q_dict[e] & tempQ
                
            # print 'expr1=[%s][%s]=='%(expr[0],e),q_dict[e]
        # print fml,'3---------------'
        if ' ' not in fml.strip():break
        if icount>maxcount:break
    if e and e in q_dict and q_dict[e]:
        return q_dict[e]
    else:
        return Q()

    
def fliter_2_json_page_continue(REQ, filter_dict):
    conn_or = Q()
    conn_and = Q()
    
    for key in filter_dict:
        and_dict = {}
        or_dict = {}
        op = ''
        temp = key.split('_')[0]
        op = temp+'_op'
        
        if REQ.has_key(op) == False:
            REQ[op] = 'and'
            
        if key == 'IsFactory__isnull':
            if filter_dict[key] == 'False':
                filter_dict[key] = True
                and_dict[key] = filter_dict[key]
                conn_and.add(Q(**and_dict), 'AND')
            elif filter_dict[key] == 'True':
                filter_dict[key] = False
                and_dict[key] = filter_dict[key]
                conn_and.add(Q(**and_dict), 'AND')
            elif 'false' in filter_dict[key] and 'true' in filter_dict[key]:
                or_dict[key] = True
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict[key] = False
                conn_or.add(Q(**or_dict), 'OR')
        elif 'FuzzyQuery' in key: #Key/SKU Number/Components/Assignee/Reporter/SKU Tracker/Agile/Customers/Work Package
            if filter_dict[key] != '':
                or_dict['Key__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['SkuNumber__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['Components__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['Assignee__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['Reporter__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['ProjID__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['AgileID__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['Customers__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
                or_dict = {}
                or_dict['WorkPackage__iregex'] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')
            else:   
                and_dict['Key__iregex'] = 'OEMPRI'
                conn_and.add(Q(**and_dict), 'AND')
        else:                            
            if REQ[op] == 'and':
                and_dict[key] = filter_dict[key]
                conn_and.add(Q(**and_dict), 'AND')
            elif REQ[op] == 'or':
                or_dict[key] = filter_dict[key]
                conn_or.add(Q(**or_dict), 'OR')

    return conn_and & conn_or
    
def filter_2_json_page(tbobj,REQ):
    pageindex = (0 if 'page' not in REQ else int(REQ['page']))
    pagesize = (30 if 'pagesize' not in REQ else int(REQ['pagesize']))
    if 'filter_keys' in REQ and REQ['filter_keys']:
        filter_dict={}
        for keyop in REQ['filter_keys'].split(','):
            key = keyop.split('_')[0]
            if key in REQ and REQ[key]:
                if '__in' in keyop:
                    if REQ[key].split(';')[0] != '':
                        filter_dict[keyop] = REQ[key].split(';')
                        if 'NULL' in filter_dict[keyop]:
                            filter_dict[keyop]+=[None,'']
                            kdict={'%s__isnull'%key:True}
                            ndict={'%s'%key:''}
                            tbobj.objects.filter(**kdict).update(**ndict)

                elif '__range' in keyop:
                    value = REQ[key].split(';')
                    if value[0] != '' or value[1] != '':
                        if value[0] == '' :
                            temp = keyop.replace('range', 'lte')
                            filter_dict[temp] = value[1]
                        elif value[1] == '':
                            temp = keyop.replace('range', 'gte')
                            filter_dict[temp] = value[0]
                        else:
                            filter_dict[keyop] = value
                else:
                    filter_dict[keyop]=REQ[key]
            elif 'FuzzyQuery' in key:
                filter_dict[keyop]=REQ[key]
                
        if 'filter_fmls' in REQ and len(REQ['filter_fmls'])>0:
            conn_and=calc_Q_express(REQ['filter_fmls'],filter_dict)
            # logging.debug(REQ['filter_fmls'])
            # logging.debug(filter_dict)
            # logging.debug(conn_and)
        else:
            conn_and=fliter_2_json_page_continue( REQ, filter_dict)
        data = tbobj.objects.filter(conn_and)
    else:
        data = tbobj.objects.all()
    if 'sortname' in REQ and 'sortorder' in REQ and REQ['sortorder'] and REQ['sortname']:
        if   REQ['sortname']=='Key' and 'Key' in REQ:REQ['sortname']='iKey'
        elif REQ['sortname']=='iKey' and 'Key' not in REQ:REQ['sortname']='Key'
        order_lst,sortnames,sortorders=[],REQ['sortname'].split(','),REQ['sortorder'].split(',')
        for i in range(len(sortnames)):
            sortorder='asc' if i>=len(sortorders) else sortorders[i]
            order_str = sortnames[i] if sortorder=='asc' else '-%s'%sortnames[i]
            order_lst.append(order_str)
        
        if 'Key' in REQ :
            if 'FWTOOLS' in REQ['Key'].upper():pos=9 #'FWTOOLS-'
            elif 'QTI' in REQ['Key'].upper():  pos=9 #'QTI9X28-'
            else:                              pos=8 #'OEMPRI-'
            data = data.annotate(
                _Key1 = Func(F('Key'),pos, function='SUBSTRING'),
                iKey = Func(F('_Key1'),6,Value('0'), function='LPAD'),
                ).order_by(*order_lst)
        else:
            data = data.order_by(*order_lst)
    jsontext = rowsobj_2_json_page(data, tbobj._meta.fields, pageindex=pageindex, pagesize=pagesize)
    return jsontext

def rowsobj_2_json_page(alldata,fields,pageindex=0,pagesize=0):
    # alldata = tbobj.objects.all()
    totalsize = alldata.count()
    pagestart = totalsize
    if totalsize==0:
        jsontext={'Rows':[],'Total':totalsize}
        return jsontext
    if pageindex > 0 and pagesize > 0:
        while pagestart>=totalsize:
            pagestart = (pageindex - 1) * pagesize
            pageindex-=1
        pageend = pagestart + pagesize
    else:
        pagestart = 0
        pageend = pagesize
    rangedata = alldata[pagestart:pageend]
    jsontext = rowsobj_2_json(rangedata, fields, total=totalsize, pageindex=pageindex, pagesize=pagesize)
    return jsontext

def rowsobj_2_json(rowsobj,fields,total=-1,pageindex=-1,pagesize=-1):
    jsonlist=[]
    jsontext={}
    for rowobj in rowsobj:
        rowtext = rowobj_2_json(rowobj, fields, todict=True)
        jsonlist.append(rowtext)
    if total==-1:total=len(jsontext)
    jsontext['Rows']=jsonlist
    if not total==-1:jsontext['Total']=total
    if not pageindex==-1:jsontext['page']=pageindex
    if not pagesize==-1:jsontext['pagesize']=pagesize
    return jsontext


def rowobj_2_json(rowobj,fields,todict=True):
    rowtext = {} if todict else []
    for f in fields:
        colval = getattr(rowobj, f.name)
        ftype=str(type(f))
        if colval is None: colval = ''
        if 'CharField' in ftype or 'TextField' in ftype:
            if colval:colval1 = colval.strip('""')
            colval1 = '"%s"'%colval
        elif 'DateTimeField' in ftype:
            colval1 = '"%s"'%(str(colval).split('.')[0].replace(' 00:00:00',''))
        else:
            colval1 = '"%s"' % colval
        if todict:
            rowtext[f.name] = colval1.strip('""') if 'AutoField' not in ftype else colval
        else:
            rowtext.append( '"%s":%s' % (f.name, colval1) )
    rowtext = rowtext if todict else '{%s}'%(','.join(rowtext))
    return rowtext

def add_new_data(request,tbobj=None,cdict={}):
    tb=tbobj.__name__.lower()
    if tb=='sku_list':
        return add_new_sku(request,tbobj=tbobj,cdict=cdict)
    elif tb=='qti_list':
        return add_new_qti(request,tbobj=tbobj,cdict=cdict,Key='Key')
    else:
        cdict['__err__']='not such table %s'%tb
        return 1,cdict['__err__']

def add_new_qti(request,tbobj=None,cdict={},Key='Key'):
    Key_dict = {Key:cdict[Key]}
    if Key_dict and tbobj.objects.filter(**Key_dict).exists():
        print 'Key exist:',cdict[Key],cdict
        update_data(request,tbobj,Key_dict,cdict)
    else:
        print 'Key insert:', cdict[Key],cdict
        create_data(request,tbobj, cdict)
    return 0,'ok'


def add_new_sku(request,tbobj=None,cdict={}):
    valid_sku = is_valid_sku(cdict['SKU'])
    if valid_sku and tbobj.objects.filter(SKU=cdict['SKU']).exists():
        print 'sku exist:',cdict['SKU'],cdict
        update_data(request,tbobj,{'SKU':cdict['SKU']},cdict)
    elif not valid_sku and tbobj.objects.filter(SKU=cdict['SKU'],CarrierPN=cdict['CarrierPN']).exists():
        print 'sku exist:', cdict['SKU'],cdict['CarrierPN'],cdict
        update_data(request,tbobj,{'SKU':cdict['SKU'],'CarrierPN':cdict['CarrierPN']},cdict)
    else:
        print 'sku insert:', cdict['SKU'],cdict['CarrierPN'],cdict
        create_data(request,request,tbobj,cdict)
    return 0,'ok'

def create_data(request,tbobj,cdict):
    p=tbobj.objects.create(**cdict)
    cdict['id']=p.id
    tb = tbobj.__name__.lower()
    desc = 'add %s: %s ' % (tb, json.dumps(cdict, ensure_ascii=False))
    add_operate_log(str(request.user), Operate='add', Result='Y', Description=desc)

def delete_data(request,tbobj,kdict):
    tbobj.objects.filter(**kdict).delete()
    tb = tbobj.__name__.lower()
    desc = 'delete : from %s , where:%s' % (tb, json.dumps(kdict, ensure_ascii=False))
    add_operate_log(str(request.user), Operate='delete', Result='Y', Description=desc)

def update_data(request,tbobj,kdict,cdict,isforce=False,islog=True):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for f in tbobj._meta.fields:
        if f.name=='UpdateDate':
            cdict[f.name] = nowtime
        elif f.name in cdict and cdict[f.name]=='' and 'DateTimeField' in str(type(f)):
            cdict.__delitem__(f.name)
    is_exist = True
    if 'id' in cdict and cdict['id']=='-1':
        cdict.__delitem__('id')
        is_exist=False
    else:
        tb = tbobj.__name__.lower()
        is_exist=False
        ndict ={};odict= {}
        for rowobj in tbobj.objects.filter(**kdict):
            ndict ={}; odict = {}
            is_exist=True
            rowdict = rowobj_2_json(rowobj, tbobj._meta.fields, todict=True)
            for f in cdict:
                try:
                    if (str(cdict[f])==str(rowdict[f]) or f=='UpdateDate') and isforce==False:continue
                except:
                    pass
                ndict[f]=cdict[f]
                odict[f]=rowdict[f]
            desc='update %s: from %s to %s, where:%s'%(tb,json.dumps(odict, ensure_ascii=False),json.dumps(ndict, ensure_ascii=False),json.dumps(kdict, ensure_ascii=False))
            if ndict and islog:add_operate_log(str(request.user), Operate='update', Result='Y', Description=desc)
        if ndict:
            # print 'update:',kdict,ndict
            if 'UpdateDate' in cdict:ndict['UpdateDate'] = nowtime
            tbobj.objects.filter(**kdict).update(**ndict)
    if not is_exist and kdict:
        # print 'add:', kdict, cdict
        create_data(request,tbobj,cdict)

def gen_description(request,tbobj,REQ):
    if 'id' not in REQ or REQ['id']=='-1':
        return ''
    Description=tbobj.objects.filter(id=REQ['id']).values('Description')
    if Description:Description=Description[0]['Description']
    Update_desc={}
    for f in tbobj._meta.fields:
        if f.name in REQ:
            Update_desc[f.name]=REQ[f.name]
    Description='%s %s update to %s\n%s'%(mytime(),request.user,json.dumps(Update_desc),Description)
    REQ['Description']=Description
    return Description

def rowcol2dict(request,rows,cols=None,isstr=False,head=0,tbobj=None,addfucn=None):
    if not cols:cols=rows[head]
    # print 'cols:',cols
    # print 'rows:',rows
    retrows=[]
    for line in rows[head+1:]:
        i=0
        cdict={}
        for col in line:
            cdict[cols[i]]=col
            i+=1
            if i>=len(cols):break
        if tbobj and addfucn:
            rets=addfucn(request,tbobj,cdict)

        if isstr:cdict=str(cdict)
        retrows.append(cdict)
    return retrows

def rowcol2csvtxt(rows,addid=False):
    csvtxt,id='',0
    for line in rows:
        if addid:
            csvtxt += ('%02d,'%id+','.join(line) + '\n')
        else:
            csvtxt += (','.join(line) + '\n')
        id += 1
    return csvtxt

def csvtxt2rowcol(csvtxt):
    lines = re.split(r'[\r\n]+', csvtxt)
    # title = lines[0].split('\t')
    title = re.split(r'[\t\,\;]+',lines[0])
    curline= ''
    rows=[]
    rows.append(title)
    for line in lines[1:]:
        if not line:continue
        cols = line.split('\t')
        if len(title)>len(cols):
            curline+=line
            cols = curline.split('\t')
        if len(title)>len(cols):continue
        rows.append(cols)
        curline=''
    return rows

def add_operate_log(UserName,Operate='login',Result='Y',Description=''):
    if not cfg_dict['LogUser']:return
    if not UserName:UserName = cfg_dict['UserName']
    op_dict={'UserName':UserName,'Operate':Operate,'Result':Result,'Description':Description,'UpdateDate':mytime()}
    logging.info(op_dict)
    Operate_List.objects.create(**op_dict)

def LogUser_Off(bak=False):
    if bak:cfg_dict['LogUser_bak']=cfg_dict['LogUser']
    cfg_dict['LogUser']=False

def LogUser_On(bak=False):
    if bak:cfg_dict['LogUser']=cfg_dict['LogUser_bak']
    else:cfg_dict['LogUser']=True

def mytime(fmt="%Y-%m-%d %H:%M:%S"):
    return time.strftime(fmt, time.localtime())
def mytimex(fmt="%Y%m%d%H%M%S"):
    return time.strftime(fmt, time.localtime())

def get_tables():
    return [m._meta.model_name.lower() for m in APPS.get_models()]

def is_valid_table(tb):
    return tb.lower() in get_tables()

def is_valid_sku(sku):#1103494/9101001/NA
    if sku.isdigit() and len(sku)==7 and sku[0:3]=='110':
        return True
    else:
        return False

def mylog(cont='',file_path='',mode='a+',time=True,client=True):
    if not file_path: 
        file_path=os.path.join(BASE_DIR,'pri_sys.log')
    if client:
        if 'CLIENTNAME' in os.environ:CLIENTNAME=os.environ['CLIENTNAME']
        elif 'HOSTNAME' in os.environ:CLIENTNAME=os.environ['HOSTNAME']
        else:CLIENTNAME='NONE'
        cont='[%s]%s'%(CLIENTNAME,cont)
    if time:
        cont='[%s]%s'%(mytime(),cont)
    cont='%s%s'%('\n',cont)
    mode=mode.lower()
    if 'w' in mode or 'a' in mode:
        dir=os.path.dirname(file_path)
        if dir and not os.path.exists(dir):os.makedirs(dir)
        writer = open(file_path, mode)
        writer.write(cont)
        writer.close()
    else:
        if not os.path.exists(file_path):
            cont=''
        else:
            reader = open(file_path, mode)
            cont = reader.read()
            reader.close()
    return cont
        
def test_sys_cmd(request):
    context        = {'err':'','rlt':'','id':'-1','template':'','fmt':'','issucc':'1'}
    REQ = {'tb':'','op':'query','fmt':'','ext':'','cmd':''}
    REQ = parsepath(request,REQ,tolower=False)
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'sys_cmd.htm')
    if not pri_is_authenticated(request):
        context['rlt'] = err_dict['not_login']
    elif not pri_is_inGroup(request, 'admins'):
        context['rlt'] = err_dict['not_permit']
    else:
        import sys_cmd
        if hasattr(sys_cmd,'exec_'+REQ['op']):
            ret,rpt = getattr(sys_cmd,'exec_'+REQ['op'])()
        elif REQ['op']=='svn_update':
            ret,rpt = sys_cmd.exec_svn_update()
        elif REQ['op']=='migrate_pri_db':
            ret,rpt = sys_cmd.exec_migrate_PRI_DB()
        elif len(REQ['cmd'])>0:
            ret,rpt = sys_cmd.exec_cmd(REQ['cmd'])
        else:
            ret,rpt = -1,''
        if not ret==-1:
            context['rlt'] = 'retcode: %s, cmd: %s\nreport:\n%s'%(ret,REQ['cmd'],rpt)
            add_operate_log(str(request.user), Operate='cmd', Result=('Y' if ret==0 else 'N'), Description=context['rlt'])
    context['cmd']=REQ['cmd']
    context['op']=REQ['op']
    return render(request, template, context)

