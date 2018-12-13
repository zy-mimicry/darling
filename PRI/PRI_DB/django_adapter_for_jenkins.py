# coding=utf-8  
import os,shutil
import sys
import argparse
import django
import traceback
 
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PRI_System.settings")
django.setup()
from PRI_DB.models import *  
from views import *
import tasks 
from tasks import *

reload(sys)  
sys.setdefaultencoding('utf-8')
import jira
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../../lib')))
from myjira import *
import time
import multiprocessing

def start_build_one_click_spkg(jira_id='',env='',job_name='',paradict={},isjar=False):
    os.system('taskkill /im excel.exe /f ')
    one_click_Jenkins_automation_path=os.path.realpath('..\..\one-click-tool-for-pkg-upgrading\one_click_Jenkins_automation')
    if not os.path.exists(one_click_Jenkins_automation_path):
        one_click_Jenkins_automation_path=os.path.realpath('..\one-click-tool-for-pkg-upgrading\one_click_Jenkins_automation')
    sys.path.append(one_click_Jenkins_automation_path)
    import one_click_Jenkins_automation
    if not jira_id and 'Key' in paradict:jira_id=paradict['Key']
    if not env and 'env' in paradict:env=paradict['env']
    queueId,desc=one_click_Jenkins_automation.auto_build(jira_id=jira_id,mylabel=env,buildfunc=None if isjar else tasks.server.build_job,job_name=job_name,paradict=paradict)
    os.system('taskkill /im excel.exe /f ')
    print 'queueId=',queueId
    print 'desc=',desc
    return queueId,desc
def start_release_check_oempri(jira_id='',env='',job_name='',paradict={}):
    queueId,desc=tasks.server.build_job(job_name,paradict),'start %s success'%(job_name)
    print 'queueId=',queueId
    print 'desc=',desc
    return queueId,desc
def start_build_spkg_oempri(jira_id='',env='',job_name='',paradict={}):
    info={}
    if not jira_id and 'JiraId' in paradict:jira_id=paradict['JiraId']
    if not env and 'env_label' in paradict:env=paradict['env_label']
    infos=find_jira_oempri(oempri_id=jira_id,getSkutracker=False,getAgile=False,getHistory=False,cmptool=False)
    info=infos[jira_id]
    if 'Components' not in info:
        Components=''
        queueId,desc=-1,'Components not exist in ticket %s'%(jira_id)
    else:
        Components=('%s'%info['Components']).upper()
        if 'AR758' in Components or 'AR858' in Components: Product='9x28'
        elif 'AR759' in Components: Product='9x40'
        elif 'AR755' in Components or 'AR865' in Components: Product='9x15'
        else: Product=''
        paradict['Product']=Product
        paradict['Output']=table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
        paradict['Config']=paradict['Output']
        paradict['JiraId']=''
        Configs=get_spkg_path(paradict['Output'],'.xml')
        # print 'Output=',paradict['Output']
        # print 'Configs=',Configs
        if Configs:paradict['Config']=Configs[0]
        if paradict['Product']:
            # queueId,desc=-1,'Components not exist in ticket %s'%(jira_id)
            queueId,desc=tasks.server.build_job(job_name,paradict),'start %s success'%(job_name)
        else:
            queueId,desc=-1,'Components not exist in 9x15/9x28/9x40'
    print 'queueId=',queueId
    print 'desc=',desc
    return queueId,desc
def start_test_spkg_oempri(jira_id='',env='',job_name='',paradict={}):
    if not jira_id and 'JiraId' in paradict:jira_id=paradict['JiraId']
    if not env and 'env_label' in paradict:env=paradict['env_label']
    paradict['JiraId']=''
    paradict['Output']=table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
    queueId,desc=tasks.server.build_job(job_name,paradict),'start %s success'%(job_name)
    print 'queueId=',queueId
    print 'desc=',desc
    return queueId,desc
def start_send_release_note(jira_id='',env='',job_name='',paradict={}):
    if not jira_id and 'JiraId' in paradict:jira_id=paradict['JiraId']
    if not env and 'env_label' in paradict:env=paradict['env_label']
    # paradict['JiraId']=''
    paradict['Destination_VERSION_Path']=table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
    ReleasePath,info,infox=get_base_release_spkg_path_from_db(jira_id)
    if info and 'ReleasePath' in info and info['ReleasePath']:
        paradict['Source_VERSION_Path']=info['ReleasePath']
    elif ReleasePath:
        paradict['Source_VERSION_Path']=os.path.dirname(ReleasePath)
    if 'Source_VERSION_Path' in paradict and paradict['Source_VERSION_Path']:
        queueId,desc=tasks.server.build_job(job_name,paradict),'start %s success'%(job_name)
        print 'queueId=',queueId
        print 'desc=',desc
    else:
        queueId,desc=-1,'can not find the base version'
    return queueId,desc
def pre_test_field_spkg_oempri(row,item_dict,jira_id):
    Output=table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
    # Output=r'\\cnshz-ev-int-10\UserData\OEMPRI\%s-test'%(jira_id)
    test_script=os.path.join(Output,'test_script.txt')
    test_script_bak=os.path.join(Output,'test_script.txt.bak')
    test_script_bak1=os.path.join(Output,'test_script.txt.field')
    queueId,desc=0,''
    ReleasePath,info,infox=get_base_release_spkg_path_from_db(jira_id)
    if ReleasePath :#jira_id in infos:
        SKUNumber=info['SKUNumber']
        queueId,desc=0,'release path for %s(%s) %s'%(SKUNumber,jira_id,ReleasePath)
        shutil.copyfile(test_script,test_script_bak) #backup test_script
        if os.path.exists(test_script_bak1):
            shutil.copyfile(test_script_bak1,test_script)  #from test_script.field
        else:
            set_spkg_field_test_flag(test_script,ReleasePath) #modify
            shutil.copyfile(test_script,test_script_bak1)  #backup test_script.field
    else:
        queueId,desc=-1,'not release path for %s'%(jira_id)
    return queueId,desc
def post_test_field_spkg_oempri(row,item_dict,jira_id):
    Output=table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
    # Output=r'\\cnshz-ev-int-10\UserData\OEMPRI\%s-test'%(jira_id)
    test_script=os.path.join(Output,'test_script.txt')
    test_script_bak=os.path.join(Output,'test_script.txt.bak')
    queueId,desc=0,''
    if os.path.exists(test_script_bak):
        shutil.copyfile(test_script_bak,test_script) 
        os.remove(test_script_bak)
    return queueId,desc
def set_spkg_field_test_flag(test_script,ReleasePath):
    test_cont=myfile(test_script)
    test_cont,c=re.subn(r'--initial_download=[^\r\n]+',r'--initial_download=%s'%(ReleasePath.replace('\\','\\\\')),test_cont,flags=re.M|re.S|re.DOTALL)
    if c==0:test_cont=re.sub(r'([\r\n]+## Optional ##[\r\n]+)',r'\1--initial_download=%s\n'%(ReleasePath.replace('\\','\\\\')),test_cont,flags=re.M|re.S|re.DOTALL)
    test_cont=re.sub(r'--option=\d+',r'--option=13',test_cont)
    myfile(test_script,test_cont,'w')
def get_base_release_spkg_path_from_db(jira_id):
    ReleasePath,info,infox='',None,None
    infos=find_jira_oempri(oempri_id=jira_id,getSkutracker=False,getAgile=False,getHistory=False,cmptool=False)
    if jira_id in infos:
        info=infos[jira_id]
        SKUNumber=info['SKUNumber']
        SkuReleasePath='' if 'ReleasePath' not in info else info['ReleasePath']
        if not ReleasePath and 'Description' in info:
            base_version_obj=re.search(r'base_version=([^\r\n]+)',str(info['Description']),flags=re.I)
            if base_version_obj:ReleasePath=base_version_obj.group(1)
        if not ReleasePath and 'Review-Notes' in info:
            base_version_obj=re.search(r'base_version=([^\r\n]+)',str(info['Review-Notes']),flags=re.I)
            if base_version_obj:ReleasePath=base_version_obj.group(1)
        if not ReleasePath:
            info_list = Jira_List.objects.filter(SkuNumber=SKUNumber,ReleasePath__iregex=r'\\\\').order_by('-CreatedDate')
            for infox in info_list:
                if not infox.Key==jira_id:
                    if SkuReleasePath!=infox.ReleasePath:ReleasePath=infox.ReleasePath
                    break
        if ReleasePath:
            Configs=get_spkg_path(ReleasePath,'.spk')
            if Configs:ReleasePath=Configs[0]
            
    return ReleasePath,info,infox
def get_spkg_path(dir,type='.xml',files=[],level=0):
    if 1:
        if level==0:files=[]
        level+=1
        if os.path.isfile(dir):return [dir]
        for fn in os.listdir(dir):
            fp=os.path.join(dir,fn) 
            fn,ext=os.path.splitext(fp)
            if 1:
                #-------------------sku-----PN-----product-fw---sub---customer
                skuobj=re.search(r'(110\d+)_990\d+_([^_]+)_[^_]+_[^_]+_([^_]+)',fn)
            if skuobj and os.path.isdir(fp) and type.lower()=='.spk':
                get_spkg_path(fp,type=type,files=files,level=level)
                continue
            if os.path.isfile(fp):
                if skuobj and ext.lower()==type.lower():
                    if fp not in files:files.append(fp)
                    break
            if not skuobj and '.xml'==type.lower():
                #-------------------sku-----PN-----product-fw---sub---customer
                skuobj=re.search(r'(110\d+)_([^_]+)_([^_\.]+)',fn)
                if skuobj and ext.lower() in ['.xls','.xlsm']:
                    if fp not in files:files.append(fp)
                    break
    return files

if __name__ == "__main__":
    if '-test' in sys.argv:
        # print 'abc'
        paradict={"RunTest": "False", "RunDiff": "False", "JiraId": "OEMPRI-9226"}
        jira_id='OEMPRI-9226'
        # start_build_one_click_spkg('FWTOOLS-322',env='CNSHZ-ED-000054-test',paradict={})
        # start_build_one_click_spkg('FWTOOLS-322',env='CNSHZ-ED-000054-test',paradict={},isjar=True)
        # print sys.modules['tasks']
        # monitor_running_job()
        # monitor_start_stop_job()
        # start_build_spkg_oempri(jira_id,job_name='PRI-Build-Process')
        start_build_spkg_oempri('',job_name='PRI-Build-Process',paradict=paradict)
        # pre_test_field_spkg_oempri(None,None,'OEMPRI-9179')
        # post_test_field_spkg_oempri(None,None,'OEMPRI-9179')
        # print table_get_sys_config('internal_oempri_folder',r'\\cnshz-ev-int-10\UserData\OEMPRI\%s')%(jira_id)
        # print get_spkg_path(r'\\cnshz-ev-int-10\UserData\OEMPRI\%s'%jira_id,'.xml')
        # set_spkg_field_test_flag(r'\\cnshz-ev-int-10\UserData\OEMPRI\OEMPRI-9179-test\test_script - Copy.txt',r'\\cnshz-ev-int-10\UserData\OEMPRI\OEMPRI-9179-test\1104152_9908590_AR7582_01.06.01.00_00_MM_001.011_000_101103963\1104152_9908590_AR7582_01.06.01.00_00_MM_001.011_000_101103963.spk')
        