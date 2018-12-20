"""AcisWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import (views,
               views_of_rex,
               views_of_shw,
               views_of_FT)

app_name = 'AcisDB'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('FT_table/', views_of_FT.FT_index, name = "FT_index"),

    # >Debug Page<
    path('rex_test/', views_of_rex.rex_jump, name = 'rex_test'),
    path('shw_test/', views_of_shw.shw_jump, name = 'shw_test'),
]
