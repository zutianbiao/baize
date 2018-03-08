#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统APP_web应用的url路由文件


###################################################################################################
from django.conf.urls import patterns, url
import APP.APP_proxy.views as views

urlpatterns = [
    url(r'/reciver', views.reciver),
    url(r'remote_control', views.remote_control),
    url(r'^/asset_manage/property/query/history', views.asset_manage_property_query_history),
    url(r'^/network_detect/task/query/history', views.network_detect_task_query_history),
    url(r'^/network_detect/task/query', views.network_detect_task_query),
    url(r'^/configure_manage/work/query_from_asset', views.configure_manage_work_query_from_asset),

]