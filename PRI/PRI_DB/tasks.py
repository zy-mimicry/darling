# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from views import *
import jenkins
from apps import PriDbConfig
from django.apps import apps as APPS
from django_apscheduler.models import DjangoJobExecution
from PRI_DB.models import * 
import time,datetime
from django.db.models import Q
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_DIR=os.path.join(BASE_DIR,'templates')
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../lib')))
from mycommon import *
import traceback,threading

import django_adapter_for_jenkins as jadapter
import jira_to_mysql as jira2mysql

jenkinsServ = 'http://cnshz-ev-int-10:8080'
jenkins_cli_jar_path = 'D:\project\jenkins-slave-for-cfg\jenkins-cli.jar'
#job_priority_dict = {'PRI-Build-Process':1,'PRI-Test-Process':2,'nv_efs_path_check':3}
server=jenkins.Jenkins(jenkinsServ)

def monitor_backup_mysql_db():
    starttime=getNowTime()
    schedule_task='backup_mysql_db'
    if set_scheduler_status(Value='running',Description='%s'%starttime,Name=schedule_task):
        try:
            if not os.path.exists('backup'):os.makedirs('backup')
            result=os.system(r'python manage.py dumpdata PRI_DB --format=json > "backup\PRI_DB(%s).json"'%(mytime(fmt='%Y-%m-%d')))
            errdesc='%s result=%s'%(getNowTime(),result)
        except:
            mylog('%s %s %s'%(schedule_task,threading.currentThread().getName(),traceback.format_exc()))
            errdesc='%s error'%getNowTime()
        set_scheduler_status(Value='finished',Description='%s'%errdesc,Name=schedule_task)
    else:
        print '%s scheduler(%s) still running or disabled ...' % (starttime,schedule_task)
def monitor_jira_2_mysql():
    starttime=getNowTime()
    schedule_task='jira_2_mysql'
    if set_scheduler_status(Value='running',Description='%s'%starttime,Name=schedule_task):
        try:
            jira2mysql.main(all=True)
            errdesc='%s'%getNowTime()
        except:
            mylog('%s %s %s'%(schedule_task,threading.currentThread().getName(),traceback.format_exc()))
            errdesc='%s error'%getNowTime()
        set_scheduler_status(Value='finished',Description='%s'%errdesc,Name=schedule_task)
    else:
        print '%s scheduler(%s) still running or disabled ...' % (starttime,schedule_task)
def monitor_jira_2_mysql_flow():
    starttime=getNowTime()
    schedule_task='jira_2_mysql_flow'
    if set_scheduler_status(Value='running',Description='%s'%starttime,Name=schedule_task):
        try:
            jira2mysql.main(flow=True)
            errdesc='%s'%getNowTime()
        except:
            mylog('%s %s %s'%(schedule_task,threading.currentThread().getName(),traceback.format_exc()))
            errdesc='%s error'%getNowTime()
        set_scheduler_status(Value='finished',Description='%s'%errdesc,Name=schedule_task)
    else:
        print '%s scheduler(%s) still running or disabled ...' % (starttime,schedule_task)
def monitor_build_job():
    starttime=getNowTime()
    schedule_task='scheduler_status'
    # mylog('%s %s monitor_build_job start'%(getNowTime(),threading.currentThread().getName()))
    if set_scheduler_status(Value='running',Description='%s'%starttime,Name=schedule_task):
        # mylog('%s %s monitor_build_job running'%(getNowTime(),threading.currentThread().getName()))
        try:
            imax=10
            while imax>=0:
                imax-=1
                monitor_build_jobex()
                time.sleep(1)
            errdesc='%s'%getNowTime()
        except:
            mylog('%s %s %s'%(schedule_task,threading.currentThread().getName(),traceback.format_exc()))
            errdesc='%s error'%getNowTime()
        endtime=getNowTime()
        set_scheduler_status(Value='finished',Description='%s'%errdesc,Name=schedule_task)
        # mylog('%s %s monitor_build_job end'%(getNowTime(),threading.currentThread().getName()))
    else:
        print '%s scheduler(%s) still running or disabled ...' % (starttime,schedule_task)
        
def monitor_build_jobex():
    monitor_running_job()
    monitor_start_stop_job()
    
def find_build_job_info(jobName, queueId):
    build_history = server.get_job_info(jobName)['builds']
    for history in build_history:
        build_Num = history['number']
        build_info = server.get_build_info(jobName, build_Num)
        # print 'history:',build_info['queueId']
        if build_info['queueId'] == queueId:
            print '| #Proj %s Progress Number is %s |' % (jobName, history['number'])
            return build_info
        else:
            continue
    return ''
    
def start_python_job(jira_id):
    job_list = Build_Job_Info.objects.filter(Q(Key=jiraid),Q(Operate='start'),~Q(JobState='done'))
    for info in job_list:
        pass
def start_jenkins_job(jiraid):
    job_list = Build_Job_Info.objects.filter(Q(Key=jiraid),Q(Operate='start')).order_by('Priority')  
    job_result={}
    last_Priority=-1
    for job_info in job_list:
        job_name = job_info.JobName
        RealName = job_info.RealName
        filter_dict={'id':job_info.id}
        if not RealName:RealName=job_name
        job_result[job_name]={'BuildResult':job_info.BuildResult,'Building':job_info.Building}
        item_dict = {}
        
        if 0:#job_info.Building in ['False']:#finished
            last_Priority=-1
            #When the high-priority job run fail, other jobs need stop
            # if job_info.BuildResult != 'SUCCESS':
                # stop_job(jiraid)
                # break
        elif job_info.Building in ['True']:#building
            last_Priority=job_info.Priority
            # break
        elif job_info.Building in [None,''] and (last_Priority==-1 or job_info.Priority==last_Priority):
            last_Priority=job_info.Priority
            # filter_dict['Key']=jiraid
            # filter_dict['Operate']='start'
            # filter_dict['JobName']=job_name
            # filter_dict['JobState']='wait'
            Depender_result=1 #1=go,0=stop,2=wait
            dpd=''
            if job_info.Depender: #depend jobname dict
                Depender=json.loads(job_info.Depender)
                for dpd in Depender:
                    if dpd in job_result and job_result[dpd]['Building']=='True':
                        Depender_result=2
                        break
                    elif dpd in job_result and job_result[dpd]['Building']=='False':
                        if Depender[dpd] and job_result[dpd]['BuildResult']!=Depender[dpd]:#not expect
                            Depender_result=0
                            break
                    else: #not exist
                        pass
            
            print '**************create***********%s %s Depende=%s'%(jiraid,job_name,Depender_result)
            if Depender_result==2:
                item_dict['BuildDesc'] = '%s wait for %s'%(getNowTime(),dpd)
            elif Depender_result==0:
                item_dict['BuildDesc'] = '%s depend by %s failed'%(getNowTime(),dpd)
                item_dict['StartDate'] = getNowTime()
                item_dict['EndedDate'] = getNowTime()
                item_dict['Building'] = 'False'
                item_dict['BuildResult'] = 'FAILURE'
            else:
                buildfunc,prefunction=None,None
                paradict={}
                queueId,errdesc=0,''
                if job_info.Job_Para:
                    Job_Para=json.loads(job_info.Job_Para)
                    try:
                        if 'function' in Job_Para and Job_Para['function'] and hasattr(jadapter,Job_Para['function']):buildfunc=getattr(jadapter,Job_Para['function'])
                        if 'paradict' in Job_Para and Job_Para['paradict']:paradict=Job_Para['paradict']
                        if 'prefunction' in Job_Para and Job_Para['prefunction'] and hasattr(jadapter,Job_Para['prefunction']):
                            prefunction=getattr(jadapter,Job_Para['prefunction'])
                            queueId,errdesc=prefunction(None,None,jiraid)
                    except:
                        queueId,errdesc=-1,'prefunction(None,None,"%s") error'%jiraid
                        print( '**************prefunction***********%s %s %s'%(jiraid,job_name,traceback.format_exc()))
                if queueId==0:
                    try:
                        if buildfunc: 
                            queueId,errdesc = buildfunc(job_name=RealName,paradict=paradict)
                        else:
                            queueId = server.build_job(RealName,paradict)
                    except:
                        queueId,errdesc=-1,'buildfunc error %s'%jiraid
                        print( '**************buildfunc***********%s %s %s'%(jiraid,job_name,traceback.format_exc()))
                item_dict['StartDate'] = getNowTime()
                item_dict['QueueId'] = queueId
                time.sleep(1)
                if queueId==-1:
                    job_info=''
                else:
                    job_info = find_build_job_info(RealName, queueId)
                if job_info != '':
                    item_dict['BuildNum'] = job_info['number']
                    item_dict['Building'] = job_info['building']
                    item_dict['BuildResult'] = job_info['result']
                    item_dict['JobUrl'] = job_info['url']
                    # item_dict['BuildEnv'] = job_info['builtOn']
                    builtOn = '' if 'builtOn' not in job_info else job_info['builtOn']
                    item_dict['BuildDesc'] = 'build on %s:%s'%(builtOn,errdesc)
                    item_dict['JobState'] = 'doing'
                else:
                    if errdesc:item_dict['BuildDesc'] = 'build result %s:%s'%('',errdesc)
                    item_dict['JobState'] = 'wait'
            # Build_Job_Info.objects.filter(**filter_dict).update(**item_dict)
        elif job_info.Building not in ['False']:
            item_dict['BuildDesc'] = '%s wait for %s'%(getNowTime(),last_Priority)
        if item_dict:set_buildjob_result(filter_dict,item_dict,jiraid)
            # break
def set_buildjob_result(filter_dict,item_dict,jiraid=''):
    if item_dict:
        Build_Job_Info.objects.filter(**filter_dict).update(**item_dict)
        list=Build_Job_Info.objects.filter(**filter_dict).order_by('-EndedDate')
        for info in list:
            if 'JobState' in item_dict and item_dict['JobState']=='done' and info.Job_Para :#post function
                Job_Para=json.loads(info.Job_Para)
                if 'postfunction' in Job_Para and Job_Para['postfunction'] and hasattr(jadapter,Job_Para['postfunction']):
                    try:
                        postfunction=getattr(jadapter,Job_Para['postfunction'])
                        postfunction(info,item_dict,jiraid)
                    except:
                        queueId,errdesc=-1,'postfunction error %s'%jiraid
                        print( '**************postfunction***********%s %s'%(jiraid,traceback.format_exc()))
    if item_dict and jiraid:
        list=Build_Job_Info.objects.filter(Key=jiraid).values('JobName','Building','BuildResult').order_by('-EndedDate')
        result_exp={}
        result_bld='SUCCESS'
        for data in list:
            JobName=data['JobName']
            if JobName not in result_exp:
                result_exp[JobName]=data['BuildResult']
                if 'True'==data['Building']:
                    result_bld='BUILDING'
                    break
                elif 'FAILURE'==data['BuildResult']:
                    result_bld=result_exp[JobName]
                    break
        if result_exp:
            Jira_List.objects.filter(Key=jiraid).update(BuildStatus=result_bld)
def set_scheduler_status(Value='running',Description='',Name='scheduler_status'):
    sysconfig=Sys_Config.objects.filter(Name=Name)
    item_dict={'Group':'Task','Name':Name,'Status':'Enabled'}
    if not sysconfig:Sys_Config.objects.create(**item_dict)
    if not table_get_sys_config('task_scheduler','True')=='True' or not table_get_sys_config_status('task_scheduler','Enabled')=='Enabled':
        print '%s task_scheduler(%s) is disabled!'%(getNowTime(),Name)
        return False
    if not sysconfig[0].Status=='Enabled':return False
    if Value=='running' and calctime(sysconfig[0].Description[:19],ret='seconds')<10:return False
    Sys_Config.objects.filter(Name=Name).update(Value=Value,Description=Description)
    return True
def stop_job_from_buildnum(jobobj):
    job_name = jobobj.JobName
    RealName = job_info.RealName
    if not RealName:RealName=job_name
    
    build_num = jobobj.BuildNum
    item_dict = {}
    item_dict['EndedDate'] = getNowTime()
    server.stop_build(RealName, build_num)
    job_info = server.get_build_info(RealName,build_num)
    
    item_dict['Building'] = job_info['building']
    item_dict['BuildResult'] = job_info['result']
    item_dict['JobState'] = 'done'
    # Build_Job_Info.objects.filter(id=jobobj.id).update(**item_dict)    
    filter_dict={'id':jobobj.id}
    set_buildjob_result(filter_dict,item_dict,jobobj.Key)
    
def stop_job_from_queueid(jobobj):
    item_dict = {}
    item_dict['EndedDate'] = getNowTime()
    if jobobj.QueueId:
        server.cancel_queue(jobobj.QueueId)
    
    item_dict['Building'] = 'False'
    item_dict['BuildResult'] = 'ABORTED'
    item_dict['JobState'] = 'done'
    # Build_Job_Info.objects.filter(id=jobobj.id).update(**item_dict)  
    filter_dict={'id':jobobj.id}
    set_buildjob_result(filter_dict,item_dict,jobobj.Key)
    
def stop_job(jiraid):
    print '**************stop job**************'
    filter_dict = {}
    filter_dict['Key'] = jiraid
    filter_dict['Building'] = 'True'
    job_list = Build_Job_Info.objects.filter(**filter_dict).order_by('Priority')
    
    for job_info in job_list:
        job_name = job_info.JobName
        if job_info.BuildNum != None:
            stop_job_from_buildnum(job_info)
        else:
            stop_job_from_queueid(job_info)
           
def monitor_jenkins_job(info):
    job_name = info.JobName
    RealName = info.RealName
    if not RealName:RealName=job_name
    id = info.id
    filter_dict={'id':id}
    item_dict = {}
    if info.BuildNum >-1:
        build_num = info.BuildNum
        job_info = server.get_build_info(RealName,build_num)
        # print job_info
        item_dict['BuildTime'] = calctime(str(info.StartDate),ret='hour')
        if job_info['building'] == False:
            item_dict['EndedDate'] = getNowTime()
            item_dict['Building'] = job_info['building']
            item_dict['BuildResult'] = job_info['result']
            item_dict['JobUrl'] = job_info['url']
            item_dict['JobState'] = 'done'
        # Build_Job_Info.objects.filter(id=id).update(**item_dict)
    elif info.QueueId>-1:
        job_info = find_build_job_info(RealName, info.QueueId)
        if job_info != '':
            item_dict['BuildNum'] = job_info['number']
            item_dict['Building'] = job_info['building']
            item_dict['BuildResult'] = job_info['result']
            item_dict['JobUrl'] = job_info['url']
            # item_dict['BuildEnv'] = job_info['builtOn']
            builtOn = '' if 'builtOn' not in job_info else job_info['builtOn']
            item_dict['Description'] = 'build on %s'%(builtOn)
            if job_info['building'] == False:
                item_dict['EndedDate'] = getNowTime()
                item_dict['JobState'] = 'done'
            else:
                item_dict['JobState'] = 'doing'
            
            # Build_Job_Info.objects.filter(id=id).update(**item_dict)
    set_buildjob_result(filter_dict,item_dict,info.Key)
                
def monitor_running_job():
    build_info_list = Build_Job_Info.objects.filter(JobState__in=['wait','doing'])
    # print '**************monitor job*************',len(build_info_list)
    for info in build_info_list:
        if info.Building in [None,'']:continue
        if info.Job_Type == 'jenkins':
            monitor_jenkins_job(info)
        
def monitor_start_stop_job():
    list=Build_Job_Info.objects.filter(JobState__in=['wait','doing']).values('Key','Operate','JobName','JobState','Job_Type').distinct()
    
    print '**************start job***************',len(list)
    if len(list) != 0:
        for data in list:
            print data
            if data['Operate'] == 'start':
                if data['Job_Type'] == 'jenkins':
                    print '**************start jenkins_job***************%s %s'%(data['Key'],data['JobName'])
                    start_jenkins_job(data['Key'])
                elif data['Job_Type'] == 'python':
                    start_python_job(data['Key'])
            elif data['Operate'] == 'stop' and data['JobState'] == 'doing':
                if data['Job_Type'] == 'jenkins':
                    print '**************stop jenkins_job***************%s %s'%(data['Key'],data['JobName'])
                    stop_job(data['Key'])
            
def build_job(request):
    context = {'err':'','rlt':'','id':'-1','template':'','fmt':'','issucc':'1'}
    REQ = {'tb':'','op':'','fmt':'','ext':''}
    REQ = parsepath(request,REQ)
    print 'REQ:',REQ

    if not REQ['tb']:
        context['err'] = err_dict['table_empty']
        return HttpResponse(context['err'], status=404)
    elif not is_valid_table(REQ['tb']):
        context['err'] = err_dict['table_notexist']%(REQ['tb'])
        return HttpResponse(context['err'], status=404)
    
    if REQ['tb'] == 'djangojobexecution':
        tbobj = DjangoJobExecution
    else:
        tbobj = APPS.get_model(PriDbConfig.name, REQ['tb'])
    
    if REQ['op'] == 'django_job_exec_list':
        result=table_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'job_info_list':
        result=job_info_list(request,tbobj,REQ,context)
    elif REQ['op'] == 'start':
        result = add_data_into_database(request,tbobj,REQ,context)
    elif REQ['op'] == 'stop':
        result = add_data_into_database(request,tbobj,REQ,context)
        
    if REQ['fmt'].lower()=='json':
        return HttpResponse(json.dumps(context['rlt'], ensure_ascii=False))
    elif not os.path.exists(context['template']):
        context['err'] = err_dict['template_notexist']%(context['template'])
        return HttpResponse(context['err'], status=404)
    else:
        return render(request, context['template'], context)
 
def getNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def myformat(srcstr,pdict):
    for x in re.findall(r'{([^\"\"\'\']+)}',srcstr):
        if x in pdict:
            srcstr=srcstr.replace('{%s}'%x,str(pdict[x]))
    return srcstr.replace("'",'"')

def repeate_excute_op(jiraid, tbobj, context, job_name):
    print '**************repeate_excute_op************',jiraid
    list = Build_Job_Info.objects.filter(Q(Key=jiraid),Q(JobName=job_name),~Q(JobState='done')).order_by('Priority')  
    if len(list) != 0:
        for job_info in list:
            job_name = job_info.JobName
            if job_info.JobState == 'doing':
                if context['op'] == 'start': context['err'] = err_dict['op_repeat'];return False                    
            elif job_info.JobState == 'wait':
                if context['op'] == 'start': context['err'] = err_dict['op_repeat'];return False
                elif context['op'] == 'stop': context['err'] = err_dict['op_fail'];return False
    else:
        if context['op'] == 'stop': context['err'] = err_dict['op_fail'];return False
        
    return True
    
def update_jobstate(jira_id,item_dict,tbobj):
    print '**************update_jobstate:',jira_id
    # filter_dict={}
    # filter_dict['Key']=jira_id
    info_list = Build_Job_Info.objects.filter(Key=jira_id)
    for info in info_list:
        filter_dict={'id':info.id}
        if info.JobState == 'doing':
            # filter_dict['JobState']='doing'
            #tbobj.objects.filter(**filter_dict).update(**item_dict)
            set_buildjob_result(filter_dict,item_dict,jira_id)
            pass
        elif info.JobState == 'wait':
            # filter_dict['JobState']='wait'
            item_dict['JobState']='done'
            item_dict['BuildResult']='ABORTED'
            # tbobj.objects.filter(**filter_dict).update(**item_dict)
            set_buildjob_result(filter_dict,item_dict,jira_id)
        else:
            continue
        if item_dict['JobState']=='done' and info.Job_Para :#post function
            Job_Para=json.loads(info.Job_Para)
            if 'postfunction' in Job_Para and Job_Para['postfunction'] and hasattr(jadapter,Job_Para['postfunction']):
                try:
                    postfunction=getattr(jadapter,Job_Para['postfunction'])
                    postfunction(info,item_dict,jira_id)
                except:
                    queueId,errdesc=-1,'postfunction error %s'%jiraid
                    item_dict['BuildDesc']=errdesc
                    print( '**************postfunction***********%s %s'%(jiraid,traceback.format_exc()))
        set_buildjob_result(filter_dict,item_dict,jira_id)
    
def add_data_into_database(request, tbobj, REQ, context):
    context['issucc'] = '0'
    context['op'] = REQ['op']
    context['tb']='' if 'tb' not in REQ else  REQ['tb']
    context['id'] = REQ['id']
    job_name_list = request.POST.getlist('job_name') 
    context['job_name'] = job_name_list
    context['env'] = '' if 'env' not in REQ else REQ['env']
    context['Parameter'] = '{}' if 'Parameter' not in REQ else REQ['Parameter']
    print 'job_name_list:', job_name_list
    
    if not pri_is_authenticated(request):
        context['err'] = err_dict['not_login']
    elif not pri_is_inGroup(request, 'admins'):
        context['err'] = err_dict['not_permit']
    else:
        if len(job_name_list) != 0:
            for job_name in job_name_list:
                #whether the jenkins job operation execution is repeated or not
                if repeate_excute_op(context['id'], tbobj, context, job_name) == True:
                    item_dict = {}
                    item_dict['Operate'] = context['op']
                    if context['op'] == 'start':
                        context['err'] = err_dict['start_build_succ']
                        jobs=Job_Info.objects.filter(JobName=job_name,Status='Enabled')
                        item_dict['JobState'] = 'wait'
                        item_dict['BuildEnv'] = context['env']
                        item_dict['Key'] = context['id']
                        Parameter=json.loads(context['Parameter'])
                        update_dict={}
                        update_dict['env']=item_dict['BuildEnv']
                        update_dict['UserName']=str(request.user) 
                        if item_dict['Key']:update_dict['Key']=item_dict['Key']
                        Job_Para=json.loads(myformat(jobs[0].Job_Para,update_dict))
                        if Parameter:#merge 2 dictionary
                            if 'paradict' in Job_Para:Job_Para['paradict'].update(Parameter)
                            else:Job_Para['paradict']=Parameter
                        item_dict['Job_Para'] = json.dumps(Job_Para)
                        item_dict['UserName'] = str(request.user)
                        item_dict['JobName'] = jobs[0].JobName
                        item_dict['Priority'] = jobs[0].Priority
                        item_dict['Depender'] = jobs[0].Depender
                        item_dict['Job_Type'] = jobs[0].Job_Type
                        item_dict['Job_Group'] = jobs[0].Job_Group
                        item_dict['RealName'] = jobs[0].RealName
                        item_dict['CreatedDate'] = getNowTime()
                        print '*********item_dict:',item_dict
                        tbobj.objects.create(**item_dict)
                        desc='start job(%s) for %s in %s'%(job_name,context['id'],context['env'])
                        add_operate_log(str(request.user), Operate='start', Result='Y', Description=desc)

                    elif context['op'] == 'stop':
                        #update Build_Job_Info operate to stop
                        update_jobstate(context['id'],item_dict,tbobj)
                        context['err'] = err_dict['stop_build_succ']
                        desc='stop job(%s) for %s'%(job_name,context['id'])
                        add_operate_log(str(request.user), Operate='stop', Result='Y', Description=desc)
        jobs=Job_Info.objects.filter(Job_Group__iregex=context['id'][0:3],Status='Enabled').order_by('Priority')
        context['joblist']= '\n'.join(["<tr><td></td><td cospan=3><label><input type='checkbox' name='job_name' value='%s'/> %s </label> </td></tr>"%(job.JobName,job.JobName) for job in jobs])
            
                
    template = os.path.join(templates_DIR, 'LigerUI', 'PRI', 'run_job.htm')
    context['template'] = template
    print '********context:',context
    return 0,''

def job_info_list(request,tbobj,REQ,context):
    print '**************job_info_list',REQ
    pageindex = (0 if 'page' not in REQ else int(REQ['page']))
    pagesize = (0 if 'pagesize' not in REQ else int(REQ['pagesize']))
    ids = REQ['id'].strip(',').split(',')
    context['id'] = ','.join(ids)
    context['template'] = table_get_template(REQ,ext='')
    print '**************context template:',context['template']
    
    job_info = tbobj.objects.filter(Key__in=ids)
    jsontext = rowsobj_2_json_page(job_info, tbobj._meta.fields, pageindex=pageindex, pagesize=pagesize)
    context['rlt'] = jsontext
    print '********context:',context
    return 0,''
