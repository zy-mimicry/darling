"""PRI_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from users import views
from PRI_DB import models as pri_db_m
from PRI_DB import views as pri_db_v
from PRI_DB import select_data
from PRI_DB import tasks
import os
from apscheduler.schedulers.background import BackgroundScheduler  
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job  


if 'scheduler' in os.environ and os.environ['scheduler']=='True':
    try:    
        #https://www.cnblogs.com/shhnwangjian/p/7877985.html
        #https://blog.csdn.net/blueheart20/article/details/70219490?locationNum=1&fps=1
        job_defaults = { 
            'coalesce': True,
            'max_instances': 1,
            'misfire_grace_time': 60
        }
        scheduler = BackgroundScheduler(job_defaults=job_defaults)  
        DjangoJobStorex=DjangoJobStore()
        DjangoJobStorex.remove_all_jobs()
        scheduler.add_jobstore(DjangoJobStorex, "default")  
        
        scheduler.print_jobs() 
        @register_job(scheduler, "interval", seconds=10,replace_existing=True)  
        def monitor_build_job():  
           tasks.monitor_build_job()
        @register_job(scheduler, "interval", minutes=5,replace_existing=True)  
        def monitor_jira_2_mysql():  
           tasks.monitor_jira_2_mysql()
        @register_job(scheduler, "interval", minutes=30,replace_existing=True)  
        def monitor_jira_2_mysql_flow():  
           tasks.monitor_jira_2_mysql_flow()
        @register_job(scheduler, "interval", days=1,replace_existing=True)  
        def monitor_backup_mysql_db():  
           tasks.monitor_backup_mysql_db()

        scheduler.print_jobs() 
        # for x in DjangoJobStorex.get_all_jobs():
            # print x
        # print dir(x)
        register_events(scheduler)
        scheduler.start()  
    except Exception as e:  
        print(e)  
        scheduler.shutdown()