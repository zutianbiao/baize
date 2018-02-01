#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动注册脚本


###################################################################################################
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from APP.APP_web.views import baize_register

if len(sys.argv) == 3:
    re = baize_register(sys.argv[1], sys.argv[2])
    print re['msg']
else:
    print u"请使用参数指定用户名称和邮箱"