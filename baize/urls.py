#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是Baize的一部分,是Baize的django url配置文件


###################################################################################################
from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^api/active_report', views.fun_active_report),
]

try:
    import APP.APP_web
    urlpatterns += [
        url(r'^web', include('APP.APP_web.urls')),
    ]
except ImportError:
    pass


try:
    import APP.APP_proxy
    urlpatterns += [
        url(r'^proxy', include('APP.APP_proxy.urls')),
    ]
except ImportError:
    pass

try:
    import APP.APP_agent
    urlpatterns += [
        url(r'^agent', include('APP.APP_agent.urls')),
    ]
except ImportError:
    pass
