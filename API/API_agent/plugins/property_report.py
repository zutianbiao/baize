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
import baize.settings as C
import logging
import API.API_agent.constant as A_C
from API.API_agent.plugins.base import request
from API.API_agent.remote_control import remote_control_capture
from API.API_agent.config_items import Config

# C_agent = Config()
# HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None)
# SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
# TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=None)


class Property_Reporter(object):
    """ 属性上报器 """
    def __init__(self):
        self.on = True

    def stop(self):
        self.on = False

    def start(self):
        cur_time = time.time() - A_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < A_C.INTERVAL_CHECK:
                time.sleep(1)
                continue
            cur_time = t
            json_property = {"name": A_C.NAME_PROPERTY}
            json_re = remote_control_capture(json_property)
            if json_re['success']:
                localtime = json_re['msg']['ansible_date_time']['epoch']
                hostname = json_re['msg']['ansible_hostname']
                sn = json_re['msg']['ansible_product_serial']
                C_agent = Config()
                if hostname != C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None):
                    HOSTNAME = C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=hostname)
                if sn != C_agent.item(item_name='SN', group_name='ASSET', default=None):
                    SN = C_agent.item(item_name='SN', group_name='ASSET', default=sn)
                if localtime != C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=sn):
                    TIME_LOCAL = C_agent.item(item_name='TIME_LOCAL', group_name='ASSET', default=localtime)
                json_re['msg']['proxy_server'] = A_C.PROXY_SERVER
                json_re['msg']['remote_control_server'] = A_C.REMOTE_CONTROL_SERVER
                json_data = {'time': localtime, 'hostname': hostname, 'sn': sn, 'data': json_re['msg']}
                msg = u"属性抓取成功"
                logger = logging.getLogger('log_file')
                logger.info(msg)
                if C.LOG_SCREEN == 'ON':
                    logger = logging.getLogger('log_screen')
                    logger.info(msg)
                url_report = A_C.URL_REPORT + 'property'
                report_re = request(url=url_report, data=json_data, timeout=300)
                if report_re['success']:
                    msg = u"属性接收成功"
                    logger = logging.getLogger('log_file')
                    logger.info(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.info(msg)
                else:
                    msg = u"属性接收失败"
                    logger = logging.getLogger('log_file')
                    logger.error(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.error(msg)
            else:
                msg = u"属性抓取失败"
                logger = logging.getLogger('log_file')
                logger.error(msg)
                if C.LOG_SCREEN == 'ON':
                    logger = logging.getLogger('log_screen')
                    logger.error(msg)

if __name__ == '__main__':
    property_reporter = Property_Reporter()
    property_reporter.start()
