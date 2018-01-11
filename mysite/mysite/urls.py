#!/usr/bin/env python
#coding=utf-8

"""mysite URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin

from mysite import views 
from mysite.west import views as west_views

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^$', views.hello),
    # url(r'^west/',west_views.hello),
    url(r'^west/staff/',west_views.staff),
    url(r'^west/templay/',west_views.templay),
    url(r'^west/form/',west_views.form),
    url(r'^west/investigate',west_views.investigate),
]