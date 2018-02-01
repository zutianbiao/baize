#!/usr/local/baize/env/bin/python
# coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件的基础类库


###################################################################################################
import os
import time
import sys
from gevent import monkey
monkey.patch_all()
import gevent
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from baize.settings import INTERVAL_WORKER
###################################################################################################


class Worker(object):
    """ 任务处理器 """
    def __init__(self):
        self._greenlet = None
        self.on = False
        self.interval = INTERVAL_WORKER

    def start(self):
        self.on = True
        if not self._greenlet:
            self._greenlet = gevent.spawn(self._loop)
            self._greenlet.join()

    def stop(self):
        self.on = False
        if self._greenlet:
            self._greenlet.kill()
            self._greenlet = None

    def do(self):
        pass

    def _loop(self):
        cur_time = time.time() - self.interval
        while self.on:
            t = time.time()
            if t - cur_time < self.interval:
                gevent.sleep(1)
                continue
            cur_time = t
            self.do()
