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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
admin.autodiscover()

from users import views
from PRI_DB import models as pri_db_m
from PRI_DB import views as pri_db_v
from PRI_DB import select_data
from PRI_DB import tasks
import settings
import os
import tasks_reg

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', pri_db_v.login),
    url(r'^$', views.LigerUI),
    url(r'test_select/', select_data.test_select),
    url(r'test_sys_cmd/', pri_db_v.test_sys_cmd),
    url(r'oempri_select/', select_data.oempri_select),
    url(r'fwtools_select/', select_data.fwtools_select),
    url(r'flow_select/', select_data.flow_select),
    url(r'factory_select/', select_data.factory_select),
]

urlpatterns += static('/LigerUI/', document_root=os.path.join(settings.BASE_DIR, 'templates/LigerUI'))
urlpatterns += [url(r'^pri_db/', pri_db_v.pri_db_operation)]
urlpatterns += [url(r'^run_job/', tasks.build_job)]
