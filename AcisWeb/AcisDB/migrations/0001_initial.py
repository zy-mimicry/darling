# Generated by Django 2.1 on 2018-12-18 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build_Job_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(blank=True, max_length=30, null=True)),
                ('Key', models.CharField(blank=True, max_length=20, null=True)),
                ('Operate', models.CharField(help_text='start,stop,restart,null', max_length=30)),
                ('JobName', models.CharField(max_length=30)),
                ('JobUrl', models.CharField(blank=True, max_length=100, null=True)),
                ('JobState', models.CharField(default='wait', help_text='done,wait,doing,handup', max_length=10)),
                ('Priority', models.IntegerField(null=True)),
                ('Depender', models.CharField(blank=True, max_length=200, null=True)),
                ('BuildNum', models.IntegerField(default=-1, null=True)),
                ('QueueId', models.IntegerField(default=-1, null=True)),
                ('Building', models.CharField(blank=True, max_length=10, null=True)),
                ('BuildResult', models.CharField(blank=True, help_text='SUCCESS,FAILED,ABORTED', max_length=10, null=True)),
                ('BuildEnv', models.CharField(blank=True, max_length=50, null=True)),
                ('BuildDesc', models.CharField(blank=True, max_length=100, null=True)),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('StartDate', models.DateTimeField(blank=True, null=True)),
                ('EndedDate', models.DateTimeField(blank=True, null=True)),
                ('BuildTime', models.CharField(blank=True, max_length=20, null=True)),
                ('Process_Id', models.CharField(blank=True, max_length=10, null=True)),
                ('Job_Type', models.CharField(blank=True, max_length=20, null=True)),
                ('Job_Group', models.CharField(blank=True, default='all', help_text='all,oempri,qti,fwtools,system', max_length=100, null=True)),
                ('RealName', models.CharField(blank=True, max_length=100, null=True)),
                ('Job_Para', models.CharField(blank=True, max_length=300, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CHECKIN_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ReviewID', models.CharField(max_length=30)),
                ('Key', models.CharField(blank=True, max_length=20, null=True)),
                ('SWIPrjName', models.CharField(blank=True, max_length=20, null=True)),
                ('SKU', models.CharField(blank=True, max_length=10, null=True)),
                ('Product', models.CharField(blank=True, max_length=10, null=True)),
                ('Customer', models.CharField(blank=True, max_length=20, null=True)),
                ('CarrierPN', models.CharField(blank=True, max_length=100, null=True)),
                ('Category', models.CharField(blank=True, help_text='Commercial,Lab,Test,NULL', max_length=20, null=True)),
                ('Apply', models.CharField(blank=True, default='N', help_text='Y,N,NULL ', max_length=1, null=True)),
                ('Suggest', models.CharField(blank=True, help_text='Y,N,NULL', max_length=1, null=True)),
                ('UserName', models.CharField(blank=True, max_length=30, null=True)),
                ('Status', models.CharField(blank=True, help_text='Reviewing,Reviewed,Merging,Merged,Testing,Tested,Closed,ERROR,NULL', max_length=10, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Jira_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Key', models.CharField(blank=True, max_length=20, null=True)),
                ('Summary', models.TextField(blank=True, null=True)),
                ('Status', models.CharField(help_text='----oempri:----,Closed,Validated,Integrated,Reviewed,Tested,Generated,In Progress,Open,----fwtools:----,done,Closed,Integrated,Checked In,In Review,Assigned,CCB,Analysis,New,To Do,In Progress', max_length=20)),
                ('CreatedDate', models.CharField(blank=True, max_length=20, null=True)),
                ('DueDate', models.CharField(blank=True, max_length=20, null=True)),
                ('Components', models.TextField(blank=True, null=True)),
                ('Assignee', models.CharField(blank=True, max_length=50, null=True)),
                ('Reporter', models.CharField(blank=True, max_length=50, null=True)),
                ('Week', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('PlanDueDate', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('IsFactory', models.CharField(blank=True, max_length=10, null=True)),
                ('SkuNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('PartNumber', models.TextField(blank=True, null=True)),
                ('ProjID', models.CharField(blank=True, max_length=10, null=True)),
                ('AgileID', models.CharField(blank=True, max_length=20, null=True)),
                ('AgileUrl', models.TextField(blank=True, null=True)),
                ('Customers', models.TextField(blank=True, null=True)),
                ('WorkPackage', models.TextField(blank=True, null=True)),
                ('BuildStatus', models.CharField(blank=True, max_length=20, null=True)),
                ('TestStatus', models.CharField(blank=True, max_length=20, null=True)),
                ('ReleasePath', models.TextField(blank=True, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Marked', models.TextField(blank=True, null=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
                ('issueType', models.CharField(blank=True, max_length=20, null=True)),
                ('Open', models.CharField(blank=True, max_length=50, null=True)),
                ('InProcess', models.CharField(blank=True, max_length=50, null=True)),
                ('Generated', models.CharField(blank=True, max_length=50, null=True)),
                ('Tested', models.CharField(blank=True, max_length=50, null=True)),
                ('Reviewed', models.CharField(blank=True, max_length=50, null=True)),
                ('Integrated', models.CharField(blank=True, max_length=50, null=True)),
                ('Validated', models.CharField(blank=True, max_length=50, null=True)),
                ('AllFilesAdded', models.CharField(blank=True, max_length=50, null=True)),
                ('SpkgValidated', models.CharField(blank=True, max_length=50, null=True)),
                ('LogValidated', models.CharField(blank=True, max_length=50, null=True)),
                ('Closed', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobName', models.CharField(max_length=30)),
                ('Job_Type', models.CharField(blank=True, default='jenkins', help_text='jenkins,cmd,python', max_length=20, null=True)),
                ('Job_Owner', models.CharField(blank=True, max_length=20, null=True)),
                ('Job_Group', models.CharField(blank=True, default='all', help_text='all,oempri,qti,fwtools,system', max_length=100, null=True)),
                ('RealName', models.CharField(blank=True, max_length=100, null=True)),
                ('Job_Para', models.CharField(blank=True, max_length=300, null=True)),
                ('Priority', models.IntegerField(default=1, null=True)),
                ('Depender', models.CharField(blank=True, max_length=200, null=True)),
                ('NeedEnv', models.CharField(blank=True, default='Yes', help_text='Yes,No', max_length=50, null=True)),
                ('Status', models.CharField(default='Enabled', help_text='Enabled,Disabled', max_length=50)),
                ('Timer', models.CharField(default='0s', help_text='0s,30s,1m,5m,10m,30m,1h,2h,1d', max_length=10)),
                ('Description', models.TextField(blank=True, null=True)),
                ('CreateDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operate_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=30)),
                ('Operate', models.CharField(help_text='login,logout,add,delete,update,other', max_length=30)),
                ('Result', models.CharField(help_text='Y,N', max_length=1)),
                ('Description', models.TextField(blank=True, null=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PCA_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product', models.CharField(blank=True, max_length=30, null=True)),
                ('Customer', models.TextField(blank=True, null=True)),
                ('SKU', models.CharField(blank=True, max_length=10, null=True)),
                ('PcaNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('PcaDesc', models.CharField(blank=True, max_length=50, null=True)),
                ('ProductId', models.CharField(blank=True, max_length=10, null=True)),
                ('FSN', models.CharField(blank=True, max_length=30, null=True)),
                ('VM', models.CharField(blank=True, max_length=50, null=True)),
                ('Result', models.CharField(blank=True, max_length=10, null=True)),
                ('TestOn', models.CharField(blank=True, max_length=30, null=True)),
                ('TestPrg', models.CharField(blank=True, max_length=30, null=True)),
                ('EnvStatus', models.CharField(default='free', help_text='busy,free', max_length=20)),
                ('MntStatus', models.CharField(default='normal', help_text='normal,error,handup', max_length=20)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
                ('Description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QTI_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Key', models.CharField(max_length=20)),
                ('Summary', models.TextField(blank=True, null=True)),
                ('CarrierCustomer', models.CharField(blank=True, max_length=100, null=True)),
                ('NV_EFS', models.TextField(blank=True, null=True)),
                ('Operation', models.CharField(blank=True, max_length=10, null=True)),
                ('Category', models.CharField(blank=True, help_text='Customer,Carrier,NULL', max_length=10, null=True)),
                ('Duplicated', models.CharField(blank=True, help_text='Y,N,NULL', max_length=10, null=True)),
                ('FixVersion', models.CharField(blank=True, max_length=100, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Status', models.CharField(blank=True, help_text='done,Closed,Integrated,Checked In,In Review,Assigned,CCB,Analysis,New,To Do,In Progress', max_length=20, null=True)),
                ('AttachStatus', models.CharField(blank=True, help_text='Ok,Error,NULL', max_length=20, null=True)),
                ('BuildStatus', models.CharField(blank=True, help_text='Building,Done,Error,NULL', max_length=20, null=True)),
                ('TestStatus', models.CharField(blank=True, help_text='Testing,Tested,Error,NULL', max_length=20, null=True)),
                ('MergeStatus', models.CharField(blank=True, help_text='Merging,Merged,Error,NULL', max_length=20, null=True)),
                ('Marked', models.TextField(blank=True, null=True)),
                ('ReviewStatus', models.CharField(blank=True, help_text='Reviewing,Reviewed,Error,NULL', max_length=20, null=True)),
                ('ReviewID', models.CharField(blank=True, max_length=50, null=True)),
                ('KeyWord', models.CharField(blank=True, max_length=50, null=True)),
                ('ApplySKU', models.TextField(blank=True, null=True)),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('DueDate', models.DateTimeField(blank=True, null=True)),
                ('Components', models.CharField(blank=True, max_length=50, null=True)),
                ('Assignee', models.CharField(blank=True, max_length=50, null=True)),
                ('Reporter', models.CharField(blank=True, max_length=50, null=True)),
                ('Week', models.DateTimeField(blank=True, null=True)),
                ('PlanDueDate', models.DateTimeField(blank=True, null=True)),
                ('RealDueDate', models.DateTimeField(blank=True, null=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewID_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ReviewID', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SKU_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CustomPrjName', models.CharField(blank=True, max_length=20, null=True)),
                ('SWIPrjName', models.CharField(max_length=20)),
                ('SKU', models.CharField(max_length=10)),
                ('PackagePN', models.CharField(blank=True, max_length=10, null=True)),
                ('Product', models.CharField(max_length=10)),
                ('Customer', models.CharField(max_length=20)),
                ('CarrierPN', models.CharField(blank=True, max_length=100, null=True)),
                ('Category', models.CharField(blank=True, help_text='Commercial,Lab,Test,NULL', max_length=20, null=True)),
                ('ParentSKU', models.CharField(blank=True, max_length=10, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
                ('PM', models.CharField(blank=True, max_length=50, null=True)),
                ('SPM', models.CharField(blank=True, max_length=50, null=True)),
                ('HPM', models.CharField(blank=True, max_length=50, null=True)),
                ('FW_Lead', models.CharField(blank=True, max_length=300, null=True)),
                ('SKU_team', models.CharField(blank=True, max_length=50, null=True)),
                ('CFG_team', models.CharField(blank=True, max_length=50, null=True)),
                ('Status', models.CharField(blank=True, help_text='Enabled,Disabled,NULL', max_length=15, null=True)),
                ('Period', models.CharField(blank=True, help_text='Obsolete,Production,Prototype,Preliminary,NULL', max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sys_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group', models.CharField(default='User', help_text='User,Jira,Jenkins,View,Task,Cmd', max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('Value', models.TextField(blank=True, null=True)),
                ('Status', models.CharField(default='Enabled', help_text='Enabled,Disabled', max_length=50)),
                ('Owner', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AcisDB.Question'),
        ),
    ]
