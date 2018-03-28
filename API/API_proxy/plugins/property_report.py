#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件中的属性上报插件


###################################################################################################
import os
import sys
import time
from gevent import monkey
monkey.patch_all()
import gevent
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from influxdb import InfluxDBClient
import API.API_proxy.constant as P_C
from API.API_proxy.plugins.base import request
from API.API_agent.config_items import Config
import baize.settings as C
import logging

# C_agent = Config()
# HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None)
# SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
# TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=None)


class Property_Summary_Reporter(object):
    """ 属性上报器 """
    def __init__(self):
        self.on = True

    def stop(self):
        self.on = False

    def start(self):
        cur_time = time.time() - P_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < P_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t
            client = InfluxDBClient(P_C.IP_INFLUXDB, P_C.PORT_INFLUXDB, P_C.USER_INFLUXDB, P_C.PASSWORD_INFLUXDB, 'property_list')
            sql = """select * from property_list where time < now() - 1m and time > now() - 5m order by time desc;"""
            try:
                sql_result = client.query(sql)
            except Exception, e:
                continue
            list_data = list()
            list_re = list(sql_result.get_points())
            if not list_re:
                continue
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
                        msg = u"更新主机%s属性信息" % sql_re['hostname']
                        logger = logging.getLogger('log_file')
                        logger.info(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.info(msg)
                        list_data.append(_dt)
            C_agent = Config()
            HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None)
            SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
            TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=None)
            if list_data and HOSTNAME:
                json_data = {'time': TIME_LOCAL, 'hostname': HOSTNAME, 'sn': SN, 'data': list_data}
                url_report = P_C.URL_REPORT + 'property'
                report_re = request(url_report, data=json_data, timeout=300)
                if report_re['success']:
                    msg = u"属性上报成功"
                    logger = logging.getLogger('log_file')
                    logger.info(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.info(msg)
                else:
                    msg = u"属性上报失败"
                    logger = logging.getLogger('log_file')
                    logger.error(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.error(msg)

if __name__ == '__main__':
    property_summary_reporter = Property_Summary_Reporter()
    property_summary_reporter.start()
