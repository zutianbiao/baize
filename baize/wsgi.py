#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是Baize的一部分,是Baize的django wsgi配置文件


###################################################################################################

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
