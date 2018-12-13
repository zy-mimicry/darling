# coding=utf-8  
import os
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
from django.db.models import Func, F, Value

reload(sys)  
sys.setdefaultencoding('utf-8')
import jira
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../../lib')))
from mycommon import *
from myjira import *
import myagile
import myPRI
import time
import multiprocessing

def jira_create_fact_subtask(tickets,user):
    create_subtasks(tickets,g_map_subtask_2_pri_status.values(),user)
def jira_close_fact_subtask(ticket,task):
    subtask=g_map_sql_status_2_pri_status[task]
    summary=g_map_subtask_2_pri_status[subtask]
    aprove_subtask(None,ticket,summary)
def jira_close_fact_subtasks(tickets,task):
    subtask=g_map_sql_status_2_pri_status[task]
    summary=g_map_subtask_2_pri_status[subtask]
    for ticket in tickets:
        aprove_subtask(None,ticket,summary)
def jira_assign_tickets(tickets,user):
    assign_ticket(tickets,user)
def update_columns_from_jira_info(info,item_dict,updatefact=False):
    if 1:
        if 1:
            if 'OempriId' in info:
                item_dict['Key'] = info['OempriId']
                # print info['OempriId'],'Resolved==',info['Resolved'],info['Status']
                if 'FWTOOLS' in info['OempriId'] and 'Resolved' in info and info['Resolved']:
                    item_dict['PlanDueDate']=info['Resolved'].split('T')[0].replace('/','-')
            if 'Summary' in info:item_dict['Summary'] = info['Summary']
            if 'Status' in info:item_dict['Status'] = info['Status']
            if 'Issue Type' in info:item_dict['issueType'] = info['Issue Type']
            if 'Created' in info:item_dict['CreatedDate'] = info['Created'].replace('/', '-')
            if info['Due Date'] != None:
                item_dict['DueDate'] = info['Due Date'].replace('/', '-')
            else:
                item_dict['DueDate'] = info['Due Date']
            if 'Components' in info:item_dict['Components'] = info['Components']
            if 'Assignee' in info:item_dict['Assignee'] = info['Assignee']
            if 'Reporter' in info:item_dict['Reporter'] = info['Reporter']
            if 'PRI-path' in info and (updatefact or info['PRI-path']):item_dict['ReleasePath'] = info['PRI-path']
            
            if 'Is Factory SPKG' in info:item_dict['IsFactory'] = info['Is Factory SPKG']
            if 'SKUNumber' in info:item_dict['SkuNumber'] = info['SKUNumber']
            if 'Part Number' in info:item_dict['PartNumber'] = info['Part Number']
            if 'ProjectId' in info and (updatefact or info['ProjectId']):item_dict['ProjID'] = info['ProjectId']
            if 'Agile' in info and (updatefact or info['Agile']):item_dict['AgileID'] = info['Agile']
            if 'AgileUrl' in info and (updatefact or info['AgileUrl']):item_dict['AgileUrl'] = info['AgileUrl']
            if 'Customers' in info:item_dict['Customers'] = info['Customers']
            if 'Work Package' in info:item_dict['WorkPackage'] = info['Work Package']
            if 'Created' in info:item_dict['CreatedDate'] = info['Created'].replace('/', '-')
            if 'Due Date' in info:    
                if info['Due Date'] != None:    
                    item_dict['DueDate'] = info['Due Date'].replace('/', '-')
                else:
                    item_dict['DueDate'] = info['Due Date']
def find_jira_oempriex(jql_str='',getAgile=False,cmptool=False):
    if 1:
        refind_count=10
        while refind_count>0:
            try:
                refind_count-=1
                prits=find_jira_oempri(jql_str=jql_str, getAgile=getAgile,cmptool=cmptool)
                break
            except Exception,e:
                prits=[]
                errtxt= str(e)
                print errtxt
                # print '1-----------------err-',errtxt,'-err--------------------2'
                jql_bak=jql_str
                tmppris=re.findall("An issue with key [\'\"]([^\'\']+)[\'\"] does not exist for field ",errtxt)
                # print '1-------------------',tmppris,'-------------------------2'
                for tmppriid in tmppris:
                    if tmppriid in jql_str:
                        jql_str=re.sub('(( *or +key=[\'\"]*%s[\'\"]*)|(key=[\'\"]*%s[\'\"]* +or *))'%(tmppriid,tmppriid),'',jql_str,flags=re.I)
                    # jql_str=jql_str.replace(' or key=%s'%tmppriid,'').replace('key=%s or '%tmppriid,'')
                # print 1,jql_bak
                # print 2,jql_str
                if jql_bak==jql_str: break
    return prits
def jira_to_mysql(filter, table_name, oempri_fwtools={}):
    print 'start process jira_to_mysql...'
    try:
        prits=find_jira_oempriex(jql_str=filter, cmptool=False)
        print len(prits)
        for id in prits:

            sub_flag = 0
            info = prits[id]
            subtasks = info['subtasks']
            # print get_subtask_passdays(subtasks)
            # break
            item_dict = {}
            for subtask in subtasks:
                if subtask.fields.summary in g_map_subtask_2_pri_status.values():
                    sub_flag = 1
                    break;
            #fresh AllFilesAdded/SpkgValidated/LogValidated
            if sub_flag == 1:
                for pristatus in g_map_pri_status_2_sql_status:
                    if pristatus in info:item_dict[g_map_pri_status_2_sql_status[pristatus]] = info[pristatus]

            list=table_name.objects.filter(Key=id).all()
            update_columns_from_jira_info(info,item_dict)
            # if 'OempriId' in info:
                # item_dict['Key'] = info['OempriId']
                # if 'FWTOOLS' in info['OempriId'] and 'Resolved' in info:
                    # item_dict['PlanDueDate']=info['Resolved'].split('T')[0].replace('/','-')
            # if 'Summary' in info:item_dict['Summary'] = info['Summary']
            # if 'Status' in info:item_dict['Status'] = info['Status']
            # if 'Issue Type' in info:item_dict['issueType'] = info['Issue Type']
            # if 'Created' in info:item_dict['CreatedDate'] = info['Created'].replace('/', '-')
            # if info['Due Date'] != None:
                # item_dict['DueDate'] = info['Due Date'].replace('/', '-')
            # else:
                # item_dict['DueDate'] = info['Due Date']
            # if 'Components' in info:item_dict['Components'] = info['Components']
            # if 'Assignee' in info:item_dict['Assignee'] = info['Assignee']
            # if 'Reporter' in info:item_dict['Reporter'] = info['Reporter']
            # if 'PRI-path' in info and info['PRI-path']:item_dict['ReleasePath'] = info['PRI-path']
            # print item_dict
            # continue
            if len(list) == 0:
                table_name.objects.create(**item_dict)
            else:
                table_name.objects.filter(Key=info['OempriId']).update(**item_dict)
    except:
        oempri_fwtools['jira_to_mysql'] = traceback.format_exc()
        print traceback.format_exc()

    print 'exit process jira_to_mysql.'
    
def factory_jira_to_mysql(filter, table_name, factory={}):
    print 'start process factory_jira_to_mysql...'
    try:
        prits=find_jira_oempriex(jql_str=filter, getAgile=True, cmptool=False)
        for id in prits:
            info = prits[id]
            list=table_name.objects.filter(Key=id).all()
            sub_flag = 0
            subtasks = info['subtasks']
            # print get_subtask_passdays(subtasks)
            # break
            item_dict = {}
            for subtask in subtasks:
                if subtask.fields.summary in g_map_subtask_2_pri_status.values():
                    sub_flag = 1
                    break;
            #fresh AllFilesAdded/SpkgValidated/LogValidated
            if sub_flag == 1:
                for pristatus in g_map_pri_status_2_sql_status:
                    if pristatus in info:item_dict[g_map_pri_status_2_sql_status[pristatus]] = info[pristatus]
            if 1:#info.has_key('Is Factory SPKG'):# and info['Is Factory SPKG'] == 'TRUE':
                update_columns_from_jira_info(info,item_dict,updatefact=True)
                # if 'OempriId' in info:item_dict['Key'] = info['OempriId']
                # if 'Summary' in info:item_dict['Summary'] = info['Summary']
                # if 'Status' in info:item_dict['Status'] = info['Status']
                # if 'Issue Type' in info:item_dict['issueType'] = info['Issue Type']
                # if 'Is Factory SPKG' in info:item_dict['IsFactory'] = info['Is Factory SPKG']
                # if 'SKUNumber' in info:item_dict['SkuNumber'] = info['SKUNumber']
                # if 'Part Number' in info:item_dict['PartNumber'] = info['Part Number']
                # if 'ProjectId' in info:item_dict['ProjID'] = info['ProjectId']
                # if 'Agile' in info:item_dict['AgileID'] = info['Agile']
                # if 'AgileUrl' in info:item_dict['AgileUrl'] = info['AgileUrl']
                # if 'Customers' in info:item_dict['Customers'] = info['Customers']
                # if 'Work Package' in info:item_dict['WorkPackage'] = info['Work Package']
                # if 'Created' in info:item_dict['CreatedDate'] = info['Created'].replace('/', '-')
                # if info['Due Date'] != None:    
                    # item_dict['DueDate'] = info['Due Date'].replace('/', '-')
                # else:
                    # item_dict['DueDate'] = info['Due Date']
                # if 'Components' in info:item_dict['Components'] = info['Components']
                # if 'Assignee' in info:item_dict['Assignee'] = info['Assignee']               
                # if 'Reporter' in info:item_dict['Reporter'] = info['Reporter']
                # if 'PRI-path' in info and info['PRI-path']:item_dict['ReleasePath'] = info['PRI-path']
                    
                if len(list) == 0:
                    table_name.objects.create(**item_dict)
                else:
                    if 1:#info.has_key('Is Factory SPKG') and info['Is Factory SPKG'] == 'TRUE':
                        table_name.objects.filter(Key=info['OempriId']).update(**item_dict)
    except:
        factory['factory_jira_to_mysql'] = traceback.format_exc()
        print traceback.format_exc()
        
    print 'exit process factory_jira_to_mysql.'
    
def qti_to_mysql(filter, table_name, qti={}):
    print 'start process qti_to_mysql...'
    try:
        prits=find_jira_oempri(jql_str=filter, cmptool=False)
        for id in prits:
            info = prits[id]
            list=table_name.objects.filter(Key=id).all()
            item_dict = {}
            temp_str = ''
            item_dict['Key'] = info['OempriId']
            item_dict['Summary'] = info['Summary']
            for version in info['FixVersion']:
                temp_str += str(version) + ','
            item_dict['FixVersion'] = temp_str[:-1]
            item_dict['Status'] = info['Status']
            item_dict['CreatedDate'] = info['Created'].replace('/', '-')
            if info['Due Date'] != None:
                item_dict['DueDate'] = info['Due Date'].replace('/', '-')
            else:
                item_dict['DueDate'] = info['Due Date']
            item_dict['Assignee'] = info['Assignee']
            item_dict['Reporter'] = info['Reporter']
            if info['Updated'] != None:
                item_dict['UpdateDate'] = info['Updated'].replace('/', '-')
            else:
                item_dict['UpdateDate'] = info['Updated']
            item_dict['Components'] = info['Components']
            #print item_dict
            
            if len(list) == 0:
                table_name.objects.create(**item_dict)
            else:
                table_name.objects.filter(Key=info['OempriId']).update(**item_dict)
    except:
        qti['qti_to_mysql'] = traceback.format_exc()
        print traceback.format_exc()
        
    print 'exit process qti_to_mysql.'
def oempriweek_to_mysql(filter, table_name, errdict={}):
    def __dict_map__(d):
        m={'Key':'OempriId','Week':'Week','PlanDueDate':'Plan due date'}
        gm=dict(zip(m.values(),m.keys()))
        r={}
        for k in d:
            if k in m:
                r[m[k]]=str(d[k])
            elif k in gm:
                r[gm[k]]=str(d[k])
        return r
    print 'start process week_to_mysql...'
    try:
        jira_to_google_spreadsheet_path = os.path.abspath(os.path.join(pathname, '../../jira_to_google_spreadsheet'))
        sys.path.insert(0, jira_to_google_spreadsheet_path)
        import jira_to_google_spreadsheet
        pris=filter.replace('key=','').split(' or ')
        prits={}
        for id in pris:
            list= table_name.objects.filter(Key=id).values('Key','Week','PlanDueDate')
            for item in list:
                prits[str(item['Key'])]=__dict_map__(item)#{'OempriId':str(item['Key']),'Week':str(item['Week']),'Plan due date':str(item['PlanDueDate'])}
        cur_cwd= os.getcwd()
        os.chdir(jira_to_google_spreadsheet_path)
        print prits
        prit1=jira_to_google_spreadsheet.update_week_with_dueday(None,pris=prits,isupdate=True)
        os.chdir(cur_cwd)
        for id in prit1:
            item_dict=__dict_map__(prit1[id])#{'Week':str(prit1[id]['Week']),'PlanDueDate':str(prit1[id]['Plan due date'])}
            print item_dict
            table_name.objects.filter(Key=id).update(**item_dict)
        errdict['desc']=''    
    except:
        errdict['desc'] = traceback.format_exc()
    print errdict['desc']
    print 'exit process week_to_mysql.'
 
def flow_jira_to_mysql(filter, table_name):
    print 'start process flow_jira_to_mysql...'
    prits=find_jira_oempri(jql_str=filter, getHistory=True, cmptool=False)
    for id in prits:
        sub_flag = 0
        info = prits[id]
        subtasks = info['subtasks']
        for subtask in subtasks:
            if subtask.fields.summary in ['update skutracker','log confirm','svt spkg and approve']:
                sub_flag = 1
                break;
        list=table_name.objects.filter(Key=id).all()
        item_dict = {}
        item_dict['issueType'] = info['Issue Type']
        item_dict['Open'] = info['Open']
        item_dict['InProcess'] = info['In Progress']
        item_dict['Generated'] = info['Generated']
        item_dict['Tested'] = info['Tested']
        item_dict['Reviewed'] = info['Reviewed']
        item_dict['Integrated'] = info['Integrated']
        item_dict['Validated'] = info['Validated']
        #fresh AllFilesAdded/SpkgValidated/LogValidated
        if sub_flag == 1:
            item_dict['AllFilesAdded'] = info['All files added']
            item_dict['SpkgValidated'] = info['Spkg validated']
            item_dict['LogValidated'] = info['Log validated']
        item_dict['Closed'] = info['Closed']
        if len(list) == 0:
            item_dict['Key'] = info['OempriId']
            item_dict['Status'] = info['Status']
            item_dict['Assignee'] = info['Assignee']
            item_dict['Reporter'] = info['Reporter']
            item_dict['CreatedDate'] = info['Created']
            table_name.objects.create(**item_dict)
        else:
            table_name.objects.filter(Key=info['OempriId']).update(**item_dict)
    print 'exit process flow_jira_to_mysql.'
    
def main(all=None,flow=None):
    my_group='stli,Layang,bhuang,mshan,nzheng'
    # last1day_jql_str='  (updated>-1d or assignee in ('+my_group+')) and ( assignee in (Layang, geyang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) or reporter in (Layang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) )  and issuetype in (standardIssueTypes(), "Carrier PRI", "Customer PRI", Action) ORDER BY key DESC, updated DESC, resolution ASC, summary DESC, cf[11518] ASC, priority DESC'
    last1day_jql_str='  (updated>-1d ) and ( assignee in (Layang, geyang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) or reporter in (Layang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) )  and issuetype in (standardIssueTypes(), "Carrier PRI", "Customer PRI", Action) ORDER BY key DESC, updated DESC, resolution ASC, summary DESC, cf[11518] ASC, priority DESC'
    fact_last1day_jql_str='project=OEMPRI and updated>-1d  and ("External issue ID" !=None or "External issue ID" !="") and (assignee in (  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) or reporter in (Layang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) ) ORDER BY key DESC, updated DESC, resolution ASC, summary DESC, cf[11518] ASC, priority DESC'
    # filter_qti = 'updated>-1d  and assignee = bhuang AND component in (PROTOCOL, CONFIG, Configuration, CONFIGURATION) AND status not in (closed, done, integrated) AND project in (qti9x28, cougar, eel, eland, qti9x40, coronado, EMU) ORDER BY status ASC, summary DESC, key ASC'
    filter_qti = '(updated>-1d  or assignee = bhuang) AND component in (PROTOCOL, CONFIG, Configuration, CONFIGURATION) AND project in (qti9x28, cougar, eel, eland, qti9x40, coronado, EMU) ORDER BY status ASC, summary DESC, key ASC'
    
    parser = argparse.ArgumentParser(description="Process input arguments for modify.py")
    parser.add_argument('-a', '--all', type=str, help='load oempri,factory,qti data to mysql')
    parser.add_argument('-f', '--flow', type=str, help='load flow data to mysql')
    if not all and not flow:
        args = parser.parse_args()
        all = args.all
        flow = args.flow
    
    if all != None:
        mgr = multiprocessing.Manager()
        oempri_fwtools = mgr.dict()
        factory = mgr.dict()
        qti = mgr.dict()
        
        p_oempri_fwtools = multiprocessing.Process(target=jira_to_mysql, args=('project in (OEMPRI, FWTOOLS) and '+last1day_jql_str, Jira_List, oempri_fwtools))
        p_factory = multiprocessing.Process(target=factory_jira_to_mysql, args=(fact_last1day_jql_str, Jira_List, factory))
        p_qti = multiprocessing.Process(target=qti_to_mysql, args=(filter_qti, QTI_List, qti))

        p_oempri_fwtools.start()
        p_factory.start()
        p_qti.start()
        p_oempri_fwtools.join()
        p_factory.join()
        p_qti.join()
        
        if len(oempri_fwtools) > 0:
            reason = ''
            for key,value in oempri_fwtools.items():
                reason += value + '\n'
            raise Exception(reason)
        
        if len(factory) > 0:
            reason = ''
            for key,value in factory.items():
                reason += value + '\n'
            raise Exception(reason)
            
        if len(qti) > 0:
            reason = ''
            for key,value in qti.items():
                reason += value + '\n'
            raise Exception(reason)
    elif flow != None:
        flow_jira_to_mysql('project=OEMPRI and '+last1day_jql_str, Jira_List)
    
def factory_jira_from_mysqlex(filter, table_name, factory={}):
    rows = table_name.objects.filter(**filter).values('Key')

    i=0
    iprg=0
    imax=rows.count()
    igo=50
    ilist=[]
    while i<imax:
        ilist.append('Key=%s'%rows[i]['Key'])
        i+=1
        if len(ilist)>=igo or i >=imax:
            iprg+=1
            tfilter=' or '.join(ilist)
            print '[%s %s/%s]------------go to do'%(iprg,i,imax),tfilter
            ilist=[]
            factory_jira_to_mysql(tfilter,table_name,factory)
def qti_from_mysqlex(filter, table_name, factory={}):
    rows = table_name.objects.filter(**filter).values('Key')

    i=0
    iprg=0
    imax=rows.count()
    igo=50
    ilist=[]
    while i<imax:
        ilist.append('Key=%s'%rows[i]['Key'])
        i+=1
        if len(ilist)>=igo or i >=imax:
            iprg+=1
            tfilter=' or '.join(ilist)
            print '[%s %s/%s]------------go to do'%(iprg,i,imax),tfilter
            ilist=[]
            jira_to_mysql(tfilter,table_name,factory)
            
def check_SKU_to_db_and_agile_file(skus,addagile=True,adddb=True,infos={},filepath=''):
    # filepath=r'D:\personnal\svn_config\Projects\lib\myagile.py.txt'
    if filepath:
        infos=sku_dict_from_file(filepath)
    count_d,count_n=0,0
    for sku in skus.split(','):
        # sku=row.SKU
        if sku and sku[0:3]=='110':
            print '%s start ot update ...'%(sku)
            info= get_skus(filter=sku,getUnit=True)
            print info
            update_sku_dict(infos,info)
            # print 'info=',info
            if addagile and filepath:
                sku_dict_2_file(filepath,infos)
            if adddb:
                update_SKU_to_db_from_agile_infos_or_file(addnew=True,update=True,infos=info,filepath='')
            count_d+=1
    print 'count_d=%s'%count_d
    return count_d
def check_SKU_in_db_to_agile_file(addnew=True,infos={},filepath=''):
    # filepath=r'D:\personnal\svn_config\Projects\lib\myagile.py.txt'
    if filepath:
        infos=sku_dict_from_file(filepath)
    count_d,count_n=0,0
    skurows=SKU_List.objects.all()
    for row in skurows:
        sku=row.SKU
        if not sku or not sku[0:3]=='110':continue
        sku_dict={sku:{'swiprj':row.SWIPrjName,'parent_sku':row.ParentSKU,'carrier':row.CarrierPN}}
        if sku not in infos:
            print '%s Product=%s, Customer=%s, Period=%s, not exist'%(sku,row.Product,row.Customer,row.Period)
            if addnew:
                info= get_skus(filter=sku,getUnit=True)
                print info
                # print 'info=',info
                if info and filepath:
                    update_sku_dict(info,sku_dict)
                    update_sku_dict(infos,info)
                    sku_dict_2_file(filepath,infos)
            count_d+=1
        elif infos[sku]:
            update_sku_dict(infos,sku_dict)
            if sku_dict and filepath:sku_dict_2_file(filepath,infos)
            
    print 'count_d=%s'%count_d
    return count_d
def update_SKU_to_db_from_agile_infos_or_file(renew=False,addnew=True,update=True,infos={},filepath=''):
    # filepath=r'D:\personnal\svn_config\Projects\lib\myagile.py.txt'
    if renew: 
        infos=get_skus(filter='all', getUnit=False, filepath=filepath)
    elif filepath:
        infos=sku_dict_from_file(filepath)
    count_d,count_n=0,0
    for sku in infos:
        skurows=SKU_List.objects.filter(SKU=sku).all()
        title=infos[sku]['title']
        status=infos[sku]['status']
        partno=''if 'partno' not in infos[sku] else infos[sku]['partno']
        titles=title.split(',')
        Product,Customer=titles[0],titles[1]
        if 'MC7354 VERIZON RADIO MODULE'==Customer:Customer='VERIZON'
        if ' ' in Product:Product=Product.split(' ')[0]
        Products=[Product]
        if 'AR858' in Product:Products.append('AR758x')
        if 'AR755' in Product:Products.append('AR755x')
        item_dict={}
        # if 'AR758' not in title:continue
        if skurows:
            if status!=skurows[0].Period or (status =='Obsolete' and not skurows[0].Category=='Test'):
                item_dict['Period']=status
                print '%s(%s %s) status(%s)!=(%s) not equal!'%(sku,status,Product,status,skurows[0].Period)
            if status not in ['Obsolete']:
                # print '%s(%s) partnumber(%s) equal!'%(sku,status,partno)
                if myPRI.isTheSameStr(Customer,skurows[0].Customer)=='' and Customer.upper() not in skurows[0].Customer.upper():
                    pass
                    item_dict['Customer']=Customer
                    print '%s(%s %s) Customer(%s)!=(%s) not equal!'%(sku,status,Product,Customer,skurows[0].Customer)
                    # print '----%s=%s=[%s]'%(Customer,skurows[0].Customer,myPRI.isTheSameStr(Customer,skurows[0].Customer))
                if skurows[0].Product not in Products and Product.upper() not in skurows[0].Product.upper():
                    item_dict['Product']=Product
                    print '%s(%s %s) Product(%s)!=(%s) not equal!'%(sku,status,Product,Product,skurows[0].Product)
                if partno and partno!=skurows[0].PackagePN :
                    item_dict['PackagePN']=partno
                    print '%s(%s %s) partNo(%s)!=(%s) not equal!'%(sku,status,Product,partno,skurows[0].PackagePN)
                    # print '%s(%s) status(%s) equal!'%(sku,status,partno)
                    # if status in ['Obsolete'] and 'AR759' in title:
                        # print '%s is %s: %s'%(sku,status,title)
                        # SKU_List.objects.filter(SKU=sku).update(Category='Test',Period=status)
            if item_dict and status in ['Obsolete']:item_dict['Category']='Test'
            if item_dict:
                count_d+=1
                pass
                # SKU_List.objects.filter(SKU=sku).update(PackagePN=partno)
                if update: SKU_List.objects.filter(SKU=sku).update(**item_dict)
            else:
                pass
                # print '%s(%s %s) is equal!'%(sku,status,Product)

        else:
            count_n+=1
            item_dict={'SKU':sku,'ParentSKU':'','Product':Product,'Customer':Customer,'Period':status,'PackagePN':partno,'Category':'Commercial','Status':'Enabled','Description':title}
            if item_dict and status in ['Obsolete']:item_dict['Category']='Test'
            if addnew: p=SKU_List.objects.create(**item_dict)
            print '%s(%s %s) not in: %s!'%(sku,status,Product,title)
            pass
    print 'diff=%s,new=%s'%(count_d,count_n)
    return count_d,count_n
def update_SKU_to_skulist_from_jiralist(filter, table_name, factory={}):
    rows = table_name.objects.filter(**filter).values('SkuNumber','PartNumber','Components','Customers','Reporter','Summary')

    i=0
    iprg=0
    imax=rows.count()
    igo=50
    ilist={}
    while i<imax:
        sku=rows[i]['SkuNumber']
        if not sku:
            i+=1
            continue
        if sku not in ilist:
            ilist[sku]={}
            # for x in ['SkuNumber','PartNumber','Components','Customers','Reporter','Summary']:
                # ilist[sku][x]=rows[i][x]
            Components=rows[i]['Components']
            Summary=rows[i]['Summary']
            if  'x' in Components.lower():
                qstr=re.sub('x.*','\\d+',Components,re.I)
                comobj=re.search(qstr,Summary)
                if comobj:
                    Components=comobj.group()
            ilist[sku]['Product'] = Components
            ilist[sku]['Category'] = 'Commercial'
            ilist[sku]['SKU'] = rows[i]['SkuNumber']
            ilist[sku]['PackagePN'] = rows[i]['PartNumber']
            ilist[sku]['Customer'] = rows[i]['Customers']
            ilist[sku]['PM'] = rows[i]['Reporter']
            ilist[sku]['Period'] = 'MOL'
            list=SKU_List.objects.filter(SKU=sku).all()
            
            if len(list) == 0:
                print '%s/%s'%(i,imax),ilist[sku]
                SKU_List.objects.create(**ilist[sku])
            elif re.search('AR755;AR855;AR865;MC;SL;HL;GTM;Q2'.replace(';','|'),Components):
                print '%s/%s exist'%(i,imax),ilist[sku]
                SKU_List.objects.filter(SKU=sku).update(**ilist[sku])
        i+=1
        # break
        # if i>200:break
    print 'sku number:%s'%len(ilist)
    # SKU_List.objects.filter(**{'Category__isnull':True}).update(Category='Commercial')
def update_jira_list_with_Week_as_PlanDueDate():
    list=Jira_List.objects.filter(Week__iregex='[0-9]')
    for row in list:
        myweek=time.strftime("%Y-%m-%d", time.strptime(row.Week, "%Y-%m-%d"))
        myplan=time.strftime("%Y-%m-%d", time.strptime(row.PlanDueDate, "%Y-%m-%d"))
        if row.Week==myweek and row.PlanDueDate==myplan:continue
        print row.Key,Jira_List.objects.filter(Key=row.Key).update(PlanDueDate=myplan,Week=myweek)
def check_sku_in_ticket_is_the_same():
    list=Jira_List.objects.filter(Key__iregex='OEMPRI-').all().order_by('-Key')
    index=0
    for row in list:
        if '_990' in str(row.Summary):
            skus=isSKUs(str(row.SkuNumber))
            skus_summary=isSKUs(str(row.Summary))
            skus_ReleasePath=isSKUs(str(row.ReleasePath))
            if skus and ((skus_summary and skus[0] not in skus_summary) or (skus_ReleasePath and skus[0] not in skus_ReleasePath)):
                index+=1
                print '%02d %s %s not in %s %s'%(index,row.Key,','.join(skus),','.join(skus_ReleasePath),row.Summary)
def test_data():
    table_name=CHECKIN_List
    # SKU_List.objects.filter(**{'Category__isnull':True}).update(Category='Commercial')
    # SKU_List.objects.filter(**{'Category__isnull':True}).update(Category='Commercial')
    # list = SKU_List.objects.filter(**{'Product__iregex':'AR758;AR759;AR858;AR755;AR855;AR865;MC;SL;HL;GTM;Q2'.replace(';','|')}).values('SKU','Product')
    # list = SKU_List.objects.values('SKU','Product').distinct()
    # list = SKU_List.objects.values('SKU','Product')
    # list=SKU_List.objects.all()
    # list=Jira_List.objects.values('issueType').distinct()
    # list=Jira_List.objects.filter(**{'Key__iregex':'fwtools'}).annotate(_iKey = Func(F('Key'),9, function='SUBSTRING')).values('_iKey','Key','CreatedDate')
    # print Jira_List.objects.filter(PlanDueDate='None').update(PlanDueDate='')
    # update_jira_list_with_Week_as_PlanDueDate()
    # pos=9
    # list=Jira_List.objects.filter(**{'Key__iregex':'fwtools'}).annotate(
    # _Key1 = Func(F('Key'),pos, function='SUBSTRING'),
    # _Key2 = Func(F('_Key1'),6,Value('0'), function='lpad'),
    # ).values('_Key1','_Key2','_Key2','Key','CreatedDate')
    # CONVERT('code',SIGNED)
    # Func(F('iKey'),Value('SIGNED'), function='CONVERT')
    # Func(Func(F('Key'),9, function='SUBSTRING'),'SIGNED', function='CONVERT')
    # Func(F('Key'),9, function='SUBSTRING')
    # list=Jira_List.objects.filter(**{'Key':'OEMPRI-8540'}).all()
    filter={
    # 'Key__iregex':'OEMPRI',
    # 'Status__iregex':'Validated|Integrated|Reviewed|Tested|Generated|In Progress|Open',
    # 'IsFactory__in':[True, 'NULL', None, ''],
    }
    # qdict = {'ReviewID': 'AR759x-20180920110040','Key':'QTI9X40-4531','SKU':'1103049','CarrierPN':'''9906910_Vodafone
# 9906910_Vodafone-IOT
# 9906831_Russia
# 9906167_GENERIC'''}
    # list = CHECKIN_List.objects.filter(**qdict)
    # list = Jira_List.objects.filter(**filter).values('Key','IsFactory','Week')
    # print list.count()
    # i=0
    # for row in list:
        # print row
        # data={}
        # for f in table_name._meta.fields:
            # data[f.name]=getattr(row,f.name)
        # if data['Category']==None:
            # i+=1
            # print i,data
    # print list.count()
    # for f in table_name._meta.fields:
        # print f.name,type(f)
        # break
    
if __name__ == "__main__":
    if '-test' in sys.argv:
        # jira_to_mysql('key=FWTOOLS-406', Jira_List) 
        # jira_create_fact_subtask('oempri-8000','Stone Li')    
        # jira_close_fact_subtask('oempri-8000','AllFilesAdded')
        # jira_close_fact_subtask('oempri-8000','SpkgValidated')
        # jira_close_fact_subtask('oempri-8000','LogValidated')
        # filter={
                # 'Key__iregex':'FWTOOLS',
                # 'Key__iregex':'OEMPRI',
                # 'ReleasePath__isnull':'',
                # 'PlanDueDate':'None',
                # 'Status__in':['Closed','done'],
        # }
        # factory_jira_from_mysqlex(filter,Jira_List)
        # update_SKU_to_skulist_from_jiralist(filter,Jira_List)
        # test_data()
        my_group='stli,Layang,bhuang,mshan,nzheng'
        last1day_jql_str='  (updated>-1d ) and ( assignee in (Layang, geyang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) or reporter in (Layang,  membersOf("All (Shenzhen Engineers)"), membersOf("! R&D - Shenzhen"), membersOf("! All (Shenzhen Employees)")) )  and issuetype in (standardIssueTypes(), "Carrier PRI", "Customer PRI", Action) ORDER BY key DESC, updated DESC, resolution ASC, summary DESC, cf[11518] ASC, priority DESC'
        jql_str='project in (OEMPRI, FWTOOLS) and '+last1day_jql_str
        prits=find_jira_oempri(jql_str=jql_str, testonly=True,cmptool=False,getSkutracker=False)
        print len(prits)
    elif '-testagile' in sys.argv:
        filepath=r'D:\personnal\svn_config\Projects\lib\myagile.py.txt'
        filepath=os.path.join(os.path.dirname(__file__), 'sku_dicct.txt')
        check_SKU_to_db_and_agile_file('1103966',addagile=True,adddb=True,infos={},filepath=filepath)
        # update_SKU_to_db_from_agile_infos_or_file(renew=True,addnew=True,update=True,infos={},filepath=filepath)
        # check_SKU_in_db_to_agile_file(addnew=True,infos={},filepath=filepath)
    else:
        main() 
