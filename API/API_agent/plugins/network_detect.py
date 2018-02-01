#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件中的网络探测插件


###################################################################################################
import sys
import os
import time
import json
from gevent import monkey
monkey.patch_all()
import gevent
import StringIO
import pycurl
import commands
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import API.API_agent.constant as A_C
from API.API_agent.plugins.base import Task_Reporter, Task_Creater, Task_Processor, request
from API.API_agent.config_items import Config
from API.API_agent.pyping import ping


class Task_Network_Detect_Creater(Task_Creater):
    """ 网络探测任务生成器 """

    def _get_tasks(self):
        C_agent = Config()
        data = {
            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None)
        }
        try:
            if data['hostname'] and data['sn']:
                response_data = request(A_C.URL_NETWORK_DETECT_TASK, data=data)
                if not isinstance(response_data, dict):
                    try:
                        response_data = eval(response_data)
                    except Exception, e:
                        response_data = json.loads(str(response_data))
                if response_data['success']:
                    if isinstance(response_data['data'], str):
                        response_data['data'] = json.loads(response_data['data'])
                    return True, response_data
                else:
                    return False, {}
            else:
                return False, {}
        except Exception, e:
            return False, {}


task_time_old = dict()
task_result = dict()


class Task_Network_Detect_Processor(Task_Processor):
    """ 网络探测任务处理 """

    def _loop(self):
        global task_result
        global task_time_old
        while self.on:
            task = self.inqueue.get()
            if isinstance(task, str):
                task = json.loads(task)
            time_now = time.time()
            if task['type'] == 'curl':
                unique_key = "%s-%d-%d-%d-%s" % (task['type'], task['source'], task['task_id'], task['target_id'], task['uri'])
                detect_key = "%s-%d-%s" % (task['type'], task['target_id'], task['uri'])
            else:
                unique_key = "%s-%d-%d-%d" % (task['type'], task['source'], task['task_id'], task['target_id'])
                detect_key = "%s-%d" % (task['type'], task['target_id'])
            if unique_key not in task_time_old:
                task_time_old[unique_key] = 0
            if detect_key not in task_result:
                task_result[detect_key] = {
                    "time_old": 0,
                    "data": {}
                }
            if task['type'] == 'ping' and time_now - task_time_old[unique_key] >= task['steps']:
                if time_now - task_result[detect_key]['time_old'] < task['steps'] and task_result[detect_key]['data']:
                    task['success'] = task_result[detect_key]['data']['success']
                    task['lost_rate'] = task_result[detect_key]['data']['lost_rate']
                    task['rtt'] = task_result[detect_key]['data']['rtt']
                    task['modtime'] = task_result[detect_key]['data']['modtime']
                else:
                    r = ping(task['target'], timeout=task['timeout'], packet_size=task['size'], count=task['num'], interval=task['interval'], quiet_output=True)
                    task['success'] = True if r.ret_code == 0 else False
                    task['lost_rate'] = r.lost_rate
                    task['rtt'] = r.avg_rtt
                    task['modtime'] = time_now
                    task_result[detect_key] = {
                        "time_old": time_now,
                        "data": task
                    }
                task_time_old[unique_key] = time_now
                del r
                self.outqueue.put(task)
            elif task['type'] == 'traceroute' and time_now - task_time_old[unique_key] >= task['steps']:
                if time_now - task_result[detect_key]['time_old'] < task['steps'] and task_result[detect_key]['data']:
                    task['success'] = task_result[detect_key]['data']['success']
                    task['data'] = task_result[detect_key]['data']['data']
                    task['modtime'] = task_result[detect_key]['data']['modtime']
                else:
                    comm = "traceroute -w %s -q %s -n %s" % (task['timeout'], task['num'], task['target'])
                    status, result = commands.getstatusoutput(comm)
                    if status == 0:
                        task['data'] = result
                        task['success'] = True
                        task['modtime'] = time_now
                        task_result[detect_key] = {
                            "time_old": time_now,
                            "data": task
                        }
                    else:
                        task['success'] = False
                        task['data'] = result
                        task['modtime'] = time_now
                        task_result[detect_key] = {
                            "time_old": time_now,
                            "data": task
                        }
                task_time_old[unique_key] = time_now
                self.outqueue.put(task)
            elif task['type'] == 'curl' and time_now - task_time_old[unique_key] >= task['steps']:
                if time_now - task_result[detect_key]['time_old'] < task['steps'] and task_result[detect_key]['data']:
                    task['success'] = task_result[detect_key]['data']['success']
                    task['time_conn'] = task_result[detect_key]['data']['time_conn']
                    task['time_total'] = task_result[detect_key]['data']['time_total']
                    task['file_size'] = task_result[detect_key]['data']['file_size']
                    task['speed'] = task_result[detect_key]['data']['speed']
                    task['modtime'] = task_result[detect_key]['data']['modtime']
                else:
                    c = pycurl.Curl()
                    if 'port' not in task:
                        port = 80
                    else:
                        port = task['port']
                    url = "http://%s:%s/%s" % (task['target'], port, task['uri'])
                    c.setopt(pycurl.URL, url)
                    b = StringIO.StringIO()
                    c.setopt(pycurl.WRITEFUNCTION, b.write)
                    c.setopt(pycurl.FOLLOWLOCATION, 1)
                    c.setopt(pycurl.USERAGENT, "Baize Agent")
                    c.setopt(pycurl.CONNECTTIMEOUT, task['timeout_conn'])
                    c.setopt(pycurl.TIMEOUT, task['timeout_total'])
                    try:
                        c.perform()
                        task['success'] = True
                        task['time_conn'] = c.getinfo(pycurl.CONNECT_TIME)
                        task['time_total'] = c.getinfo(pycurl.TOTAL_TIME)
                        task['file_size'] = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
                        task['speed'] = c.getinfo(pycurl.SPEED_DOWNLOAD)
                    except Exception, e:
                        task['success'] = False
                        task['time_conn'] = 0.00
                        task['time_total'] = 0.00
                        task['file_size'] = 0.00
                        task['speed'] = 0.00
                    task['modtime'] = time_now
                    task_result[detect_key] = {
                        "time_old": time_now,
                        "data": task
                    }
                task_time_old[unique_key] = time_now
                self.outqueue.put(task)


class Task_Network_Detect_Reporter(Task_Reporter):
    """ 网络探测任务上报器 """

    def _loop(self):

        cur_time = time.time() - A_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < A_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t
            data = self.queue.get()
            data['time'] = t
            C_agent = Config()
            json_report = {
                "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                "data": []
            }
            json_report['data'].append(data)
            print json_report
            if json_report['hostname'] and json_report['sn']:
                print self._report_tasks(data=json_report, reciver='network_detect')
            json_report['data'] = []


class Network_Detect_Task(object):
    """ 网络探测任务的抽象类 """
    def __init__(self, worknum=A_C.PROCESS_NUM):
        self.reporter = Task_Network_Detect_Reporter()
        self.creater = Task_Network_Detect_Creater()
        self.workers = []
        self.on = False
        for i in xrange(worknum):
            self.workers.append(Task_Network_Detect_Processor(self.creater.queue, self.reporter.queue))

    def start(self):
        self.on = True
        self.creater.start()
        for worker in self.workers:
            worker.start()
        self.reporter.start()
        self._loop()

    def stop(self):
        self.on = False
        self.creater.stop()
        for worker in self.workers:
            worker.stop()
        self.reporter.stop()

    def _loop(self):
        cur_time = time.time() - A_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < A_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t

if __name__ == '__main__':
    network_detect = Network_Detect_Task()
    network_detect.start()
