#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统APP_agent应用的url路由文件


###################################################################################################
from django.conf.urls import patterns, url
import APP.APP_agent.views as views

urlpatterns = [
    url(r'remote_control', views.remote_control),
]