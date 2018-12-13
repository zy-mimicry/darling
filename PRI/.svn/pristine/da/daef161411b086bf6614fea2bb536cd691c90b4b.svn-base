# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# python manage.py migrate   # 创建表结构
# python manage.py makemigrations PRI_DB  # 让 Django 知道我们在我们的模型有一些变更
# python manage.py migrate PRI_DB --fake  # 创建表结构
# python manage.py dumpdata PRI_DB --format=json > "backup\PRI_DB(%date:/=-%).json"
# add mysql client: grant all on *.* to 'root'@'hostname' identified by 'password' with grant option;
# FLUSH PRIVILEGES;

class SKU_List(models.Model):
    CustomPrjName = models.CharField(max_length=20,null=True,blank=True)
    SWIPrjName = models.CharField(max_length=20)
    SKU = models.CharField(max_length=10)
    PackagePN = models.CharField(max_length=10,null=True,blank=True)
    Product = models.CharField(max_length=10)
    Customer = models.CharField(max_length=20)
    CarrierPN = models.CharField(max_length=100,null=True,blank=True)
    Category = models.CharField(max_length=20,null=True,blank=True,help_text='Commercial,Lab,Test,NULL')
    ParentSKU = models.CharField(max_length=10,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    CreateDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateTimeField(auto_now=True)

    PM = models.CharField(max_length=50,null=True,blank=True)
    SPM = models.CharField(max_length=50,null=True,blank=True)
    HPM = models.CharField(max_length=50,null=True,blank=True)
    FW_Lead = models.CharField(max_length=300,null=True,blank=True)
    SKU_team = models.CharField(max_length=50,null=True,blank=True)
    CFG_team = models.CharField(max_length=50,null=True,blank=True)
    Status = models.CharField(max_length=15,null=True,blank=True,help_text='Enabled,Disabled,NULL')
    Period = models.CharField(max_length=15,null=True,blank=True,help_text='Obsolete,Production,Prototype,Preliminary,NULL')

class QTI_List(models.Model):
    #Key,Summary,CarrierCustomer,NV_EFS,Operation,Category,Duplicated
    Key = models.CharField(max_length=20)
    Summary = models.TextField(null=True,blank=True)
    CarrierCustomer = models.CharField(max_length=100,null=True,blank=True)
    NV_EFS = models.TextField(null=True,blank=True)
    Operation = models.CharField(max_length=10,null=True,blank=True)
    Category = models.CharField(max_length=10,null=True,blank=True,help_text='Customer,Carrier,NULL')
    Duplicated = models.CharField(max_length=10,null=True,blank=True,help_text='Y,N,NULL')

    FixVersion = models.CharField(max_length=100,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    Status = models.CharField(max_length=20,null=True,blank=True,help_text='done,Closed,Integrated,Checked In,In Review,Assigned,CCB,Analysis,New,To Do,In Progress')
    AttachStatus = models.CharField(max_length=20,null=True,blank=True,help_text='Ok,Error,NULL')
    BuildStatus = models.CharField(max_length=20,null=True,blank=True,help_text='Building,Done,Error,NULL')
    TestStatus = models.CharField(max_length=20,null=True,blank=True,help_text='Testing,Tested,Error,NULL')
    MergeStatus = models.CharField(max_length=20,null=True,blank=True,help_text='Merging,Merged,Error,NULL')
    Marked = models.TextField(null=True,blank=True)
    ReviewStatus = models.CharField(max_length=20,null=True,blank=True,help_text='Reviewing,Reviewed,Error,NULL')
    ReviewID = models.CharField(max_length=50,null=True,blank=True)
    KeyWord = models.CharField(max_length=50,null=True,blank=True)
    ApplySKU = models.TextField(null=True,blank=True)
    CreatedDate = models.DateTimeField(null=True,blank=True)
    DueDate = models.DateTimeField(null=True,blank=True)
    Components = models.CharField(max_length=50,null=True,blank=True)
    Assignee = models.CharField(max_length=50,null=True,blank=True)
    Reporter = models.CharField(max_length=50,null=True,blank=True)
    Week = models.DateTimeField(null=True,blank=True)
    PlanDueDate = models.DateTimeField(null=True,blank=True)
    RealDueDate = models.DateTimeField(null=True,blank=True)

    UpdateDate = models.DateTimeField(auto_now=True)

class ReviewID_List(models.Model):
    ReviewID = models.CharField(max_length=30)

class CHECKIN_List(models.Model):
    ReviewID = models.CharField(max_length=30)
    Key = models.CharField(max_length=20,null=True,blank=True)
    SWIPrjName = models.CharField(max_length=20,null=True,blank=True)
    SKU = models.CharField(max_length=10,null=True,blank=True)
    Product = models.CharField(max_length=10,null=True,blank=True)
    Customer = models.CharField(max_length=20,null=True,blank=True)
    CarrierPN = models.CharField(max_length=100,null=True,blank=True)
    Category = models.CharField(max_length=20,null=True,blank=True,help_text='Commercial,Lab,Test,NULL')
    Apply = models.CharField(max_length=1,null=True,blank=True,default='N',help_text='Y,N,NULL ')#Y/N
    Suggest = models.CharField(max_length=1,null=True,blank=True,help_text='Y,N,NULL')#Y/N
    UserName = models.CharField(max_length=30,null=True,blank=True)
    Status = models.CharField(max_length=10,null=True,blank=True,help_text='Reviewing,Reviewed,Merging,Merged,Testing,Tested,Closed,ERROR,NULL')
    Description = models.TextField(null=True,blank=True)

    UpdateDate = models.DateTimeField(auto_now=True)

class Operate_List(models.Model):
    UserName = models.CharField(max_length=30)
    Operate = models.CharField(max_length=30,help_text='login,logout,add,delete,update,other')
    Result = models.CharField(max_length=1,help_text='Y,N')#Y/N
    Description = models.TextField(null=True,blank=True)

    UpdateDate = models.DateTimeField(auto_now=True)
    
class Sys_Config(models.Model):
    Group = models.CharField(max_length=50,default='User',help_text='User,Jira,Jenkins,View,Task,Cmd')
    Name = models.CharField(max_length=50)
    Value = models.TextField(null=True,blank=True)
    Status = models.CharField(max_length=50,default='Enabled',help_text='Enabled,Disabled')
    Owner = models.CharField(max_length=50,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)

    CreateDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateTimeField(auto_now=True)
    
class Jira_List(models.Model):
    Key = models.CharField(max_length=20,null=True,blank=True)
    Summary = models.TextField(null=True,blank=True)
    Status = models.CharField(max_length=20,help_text='----oempri:----,Closed,Validated,Integrated,Reviewed,Tested,Generated,In Progress,Open,----fwtools:----,done,Closed,Integrated,Checked In,In Review,Assigned,CCB,Analysis,New,To Do,In Progress')
    CreatedDate = models.CharField(max_length=20,null=True,blank=True)
    DueDate = models.CharField(max_length=20,null=True,blank=True)
    Components = models.TextField(null=True,blank=True)
    Assignee = models.CharField(max_length=50,null=True,blank=True)
    Reporter = models.CharField(max_length=50,null=True,blank=True)
    Week = models.CharField(max_length=20,null=True,blank=True,default='')
    PlanDueDate = models.CharField(max_length=20,null=True,blank=True,default='')

    IsFactory = models.CharField(max_length=10,null=True,blank=True)
    SkuNumber = models.CharField(max_length=10,null=True,blank=True)
    PartNumber = models.TextField(null=True,blank=True)
    ProjID = models.CharField(max_length=10,null=True,blank=True)
    AgileID = models.CharField(max_length=20,null=True,blank=True)
    AgileUrl = models.TextField(null=True,blank=True)
    Customers = models.TextField(null=True,blank=True)
    WorkPackage = models.TextField(null=True,blank=True)

    BuildStatus = models.CharField(max_length=20,null=True,blank=True)
    TestStatus = models.CharField(max_length=20,null=True,blank=True)
    ReleasePath = models.TextField(null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    Marked = models.TextField(null=True,blank=True)
    UpdateDate = models.DateTimeField(auto_now=True)

    issueType = models.CharField(max_length=20,null=True,blank=True)
    Open = models.CharField(max_length=50,null=True,blank=True)
    InProcess = models.CharField(max_length=50,null=True,blank=True)
    Generated = models.CharField(max_length=50,null=True,blank=True)
    Tested = models.CharField(max_length=50,null=True,blank=True)
    Reviewed = models.CharField(max_length=50,null=True,blank=True)
    Integrated = models.CharField(max_length=50,null=True,blank=True)
    Validated = models.CharField(max_length=50,null=True,blank=True)
    AllFilesAdded = models.CharField(max_length=50,null=True,blank=True)
    SpkgValidated = models.CharField(max_length=50,null=True,blank=True)
    LogValidated = models.CharField(max_length=50,null=True,blank=True)
    Closed = models.CharField(max_length=50,null=True,blank=True)
        
class PCA_List(models.Model):
    # Product	Customer	SKU#	PcaNumber	PcaDesc	ProductId	FSN	VM	Result	TestOn	UpdateDate	Status
    Product = models.CharField(max_length=30,null=True,blank=True)
    Customer = models.TextField(null=True,blank=True)
    SKU = models.CharField(max_length=10,null=True,blank=True)
    PcaNumber = models.CharField(max_length=10,null=True,blank=True)
    PcaDesc = models.CharField(max_length=50,null=True,blank=True)
    ProductId = models.CharField(max_length=10,null=True,blank=True)
    FSN = models.CharField(max_length=30,null=True,blank=True)
    VM = models.CharField(max_length=50,null=True,blank=True)
    Result = models.CharField(max_length=10,null=True,blank=True)
    TestOn = models.CharField(max_length=30,null=True,blank=True)
    TestPrg = models.CharField(max_length=30,null=True,blank=True)
    EnvStatus = models.CharField(max_length=20,default='free',help_text='busy,free')
    MntStatus = models.CharField(max_length=20,default='normal',help_text='normal,error,handup')
    UpdateDate = models.DateTimeField(auto_now=True)
    Description = models.TextField(null=True,blank=True)

class Build_Job_Info(models.Model):
    UserName = models.CharField(max_length=30,null=True,blank=True)
    Key = models.CharField(max_length=20,null=True,blank=True)
    Operate = models.CharField(max_length=30,help_text='start,stop,restart,null')#start/stop
    JobName = models.CharField(max_length=30)
    JobUrl = models.CharField(max_length=100,null=True,blank=True)
    JobState = models.CharField(max_length=10,default='wait',help_text='done,wait,doing,handup')#done/wait/doing
    Priority = models.IntegerField(null=True)
    Depender = models.CharField(max_length=200,null=True,blank=True) #{'jobname':'SUCCESS'}
    BuildNum = models.IntegerField(null=True,default=-1)
    QueueId = models.IntegerField(null=True,default=-1)
    Building = models.CharField(max_length=10,null=True,blank=True)
    BuildResult = models.CharField(max_length=10,null=True,blank=True,help_text='SUCCESS,FAILED,ABORTED')
    BuildEnv = models.CharField(max_length=50,null=True,blank=True)
    BuildDesc = models.CharField(max_length=100,null=True,blank=True)
    CreatedDate = models.DateTimeField(null=True,blank=True)
    StartDate = models.DateTimeField(null=True,blank=True)
    EndedDate = models.DateTimeField(null=True,blank=True)
    BuildTime = models.CharField(max_length=20,null=True,blank=True)
    Process_Id = models.CharField(max_length=10,null=True,blank=True)
    Job_Type = models.CharField(max_length=20,null=True,blank=True)
    Job_Group = models.CharField(max_length=100,null=True,blank=True,default='all',help_text='all,oempri,qti,fwtools,system')
    RealName = models.CharField(max_length=100,null=True,blank=True)
    Job_Para = models.CharField(max_length=300,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)

class Job_Info(models.Model):
    JobName = models.CharField(max_length=30)
    Job_Type = models.CharField(max_length=20,null=True,blank=True,default='jenkins',help_text='jenkins,cmd,python')
    Job_Owner = models.CharField(max_length=20,null=True,blank=True)
    Job_Group = models.CharField(max_length=100,null=True,blank=True,default='all',help_text='all,oempri,qti,fwtools,system')
    RealName = models.CharField(max_length=100,null=True,blank=True)
    Job_Para = models.CharField(max_length=300,null=True,blank=True)
    Priority = models.IntegerField(null=True,default=1)
    Depender = models.CharField(max_length=200,null=True,blank=True)
    NeedEnv = models.CharField(max_length=50,null=True,blank=True,default='Yes',help_text='Yes,No')
    Status = models.CharField(max_length=50,default='Enabled',help_text='Enabled,Disabled')
    Timer = models.CharField(max_length=10,default='0s',help_text='0s,30s,1m,5m,10m,30m,1h,2h,1d')
    Description = models.TextField(null=True,blank=True)
    CreateDate = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    UpdateDate = models.DateTimeField(null=True,blank=True,auto_now=True)
