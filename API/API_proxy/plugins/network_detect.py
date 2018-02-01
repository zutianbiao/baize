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
from influxdb import InfluxDBClient
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import API.API_proxy.constant as P_C
from API.API_proxy.plugins.base import Task_Reporter, Task_Creater, Task_Processor, request
from API.API_agent.config_items import Config as Config_Agent


# C_agent = Config_Agent()
# HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None)
# SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
# TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=None)


class Task_Network_Detect_Summary_Creater(Task_Creater):
    """ 网络探测任务生成器 """

    def _get_tasks(self):
        client = InfluxDBClient(P_C.IP_INFLUXDB, P_C.PORT_INFLUXDB, P_C.USER_INFLUXDB, P_C.PASSWORD_INFLUXDB, 'network_detect_list')
        sql = """select * from network_detect_list  where time>now() - 5m order by time desc;"""
        try:
            sql_result = client.query(sql)
        except Exception, e:
            return False, {}
        list_data = list()
        list_re = list(sql_result.get_points())
        if not list_re:
            return False, {}
        time_old = list_re[0]['time']
        for sql_re in list_re:
            if sql_re['time'] == time_old:
                if isinstance(sql_re, dict) and sql_re.get('value'):
                    _dt = {
                        "time": int(time.mktime(time.strptime(sql_re['time'], '%Y-%m-%dT%H:%M:00Z'))) + 8 * 60 * 60,
                        "hostname": sql_re['hostname'],
                        "sn": sql_re['sn'],
                        "data": sql_re['value']
                    }
                    list_data.append(_dt)
        C_agent = Config_Agent()
        HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None)
        SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
        TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=None)
        if list_data and HOSTNAME:
            json_data = {'time': TIME_LOCAL, 'hostname': HOSTNAME, 'sn': SN, 'data': list_data}
            return True, json_data
        else:
            return False, {}


class Task_Network_Detect_Summary_Reporter(Task_Reporter):
    """ 网络探测任务上报器 """

    def _loop(self):
        while self.on:
            json_data = self.queue.get()
            if isinstance(json_data, str):
                json_data = json.loads(json_data)
            print json_data
            print self._report_tasks(data=json_data, reciver='network_detect')


class Task_Network_Detect_Summary_Processor(Task_Processor):
    """ 网络探测任务处理 """

    def _loop(self):
        while self.on:
            task = self.inqueue.get()
            self.outqueue.put(task)


class Report_Summary_Network_Detect(object):
    """ 网络探测任务的抽象类 """
    def __init__(self, worknum=P_C.PROCESS_NUM):
        self.reporter = Task_Network_Detect_Summary_Reporter()
        self.creater = Task_Network_Detect_Summary_Creater()
        self.on = False
        self.workers = []
        for i in xrange(worknum):
            self.workers.append(Task_Network_Detect_Summary_Processor(self.creater.queue, self.reporter.queue))

    def start(self):
        self.on = True
        self.creater.start()
        self.reporter.start()
        for worker in self.workers:
            worker.start()
        self._loop()

    def stop(self):
        self.on = False
        self.creater.stop()
        for worker in self.workers:
            worker.stop()
        self.reporter.stop()

    def _loop(self):
        cur_time = time.time() - P_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < P_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t

if __name__ == '__main__':
    summary_network_detect = Report_Summary_Network_Detect()
    summary_network_detect.start()
