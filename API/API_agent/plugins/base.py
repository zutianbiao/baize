#!/usr/local/baize/env/bin/python
# coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件的基础类库


###################################################################################################
import os
import time
import sys
import json
import urllib
import urllib2
import Queue
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue
import gevent
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import API.API_agent.constant as A_C

###################################################################################################


def request(url, method='POST', data={}, timeout=60):
    """ 发起http协议请求 """
    if method == 'POST':
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
    else:
        req = urllib2.Request(url=url)
    try:
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = json.loads(re)
    except Exception, e:
        return {"success": False, 'msg': str(e)}
    return re


class Task_Creater(object):
    """ 任务生成器 """
    def __init__(self, queuesize=A_C.MAX_QUEUE_SIZE):
        self.queue = Queue(maxsize=queuesize)
        self._greenlet = None

    def start(self):
        self.on = True
        if not self._greenlet:
            self._greenlet = gevent.spawn(self._loop)

    def stop(self):
        self.on = False
        if self._greenlet:
            self._greenlet.kill()
            self._greenlet.join()
            self._greenlet = None

    def prepare_task(self):
        flg, data = self._get_tasks()
        if flg:
            return data
        else:
            return {}

    def assign_task(self):
        data = self.prepare_task()
        if 'data' in data:
            for task in data['data']:
                self.queue.put(task)

    def _loop(self):
        if self.queue.qsize() <= 10:
            interval = 5
        else:
            interval = A_C.INTERVAL_CHECK
        cur_time = time.time() - interval
        while self.on:
            t = time.time()
            if t - cur_time < interval:
                gevent.sleep(1)
                continue
            cur_time = t
            self.assign_task()

    def _get_tasks(self):
        return False, {}


class Task_Processor(object):
    """ 任务处理器 """
    def __init__(self, inqueue, outqueue):
        self.inqueue = inqueue
        self.outqueue = outqueue
        self._greenlet = None

    def start(self):
        self.on = True
        if not self._greenlet:
            self._greenlet = gevent.spawn(self._loop)

    def stop(self):
        self.on = False
        if self._greenlet:
            self._greenlet.kill()
            self._greenlet.join()
            self._greenlet = None

    def _loop(self):
        pass


class Task_Reporter(object):
    """ 任务上报器 """
    def __init__(self, queuesize=A_C.MAX_QUEUE_SIZE):
        self.queue = Queue(maxsize=queuesize)
        self._greenlet = None

    def start(self):
        self.on = True
        if not self._greenlet:
            self._greenlet = gevent.spawn(self._loop)

    def stop(self):
        self.on = False
        if self._greenlet:
            self._greenlet.kill()
            self._greenlet.join()
            self._greenlet = None

    def _report_tasks(self, data, reciver):
        url_report = A_C.URL_REPORT + reciver
        return request(url_report, data=data)

    def _loop(self):
        pass
