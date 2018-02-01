#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的常量库


###################################################################################################
import os
import sys
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from API.API_proxy.config_items import Config
from APP.APP_proxy.config import *
###################################################################################################

C_proxy = Config()
# Proxy对应的influxdb地址
IP_INFLUXDB = C_proxy.item(item_name='IP_INFLUXDB', group_name='DEFAULT', default=IP_INFLUXDB, type='str')
PORT_INFLUXDB = C_proxy.item(item_name='PORT_INFLUXDB', group_name='DEFAULT', default=PORT_INFLUXDB, type='str')
USER_INFLUXDB = C_proxy.item(item_name='USER_INFLUXDB', group_name='DEFAULT', default=USER_INFLUXDB, type='str')
PASSWORD_INFLUXDB = C_proxy.item(item_name='PASSWORD_INFLUXDB', group_name='DEFAULT', default=PASSWORD_INFLUXDB, type='str')
DURATION_INFLUXDB = C_proxy.item(item_name='DURATION_INFLUXDB', group_name='DEFAULT', default=DURATION_INFLUXDB, type='str')
REPLICATION_INFLUXDB = C_proxy.item(item_name='REPLICATION_INFLUXDB', group_name='DEFAULT', default=REPLICATION_INFLUXDB, type='str')
# web server地址
WEB_SERVER = C_proxy.item(item_name='WEB_SERVER', group_name='DEFAULT', default=WEB_SERVER, type='str')
# 网络探测任务缓存时长
EXPIRE_NETWORK_DETECT_TASK = C_proxy.item(item_name='EXPIRE_NETWORK_DETECT_TASK', group_name='NETWORK_DETECT', default=EXPIRE_NETWORK_DETECT_TASK, type='str')
# 查询网络探测任务的url
URL_NETWORK_DETECT_TASK = C_proxy.item(item_name='URL_NETWORK_DETECT_TASK', group_name='NETWORK_DETECT', default=URL_NETWORK_DETECT_TASK, type='str')
# 上报地址
URL_REPORT = C_proxy.item(item_name='URL_REPORT', group_name='DEFAULT', default=URL_REPORT, type='str')
# 检查探测任务的频率(单位: 秒)
INTERVAL_CHECK = C_proxy.item(item_name='INTERVAL_CHECK', group_name='DEFAULT', default=INTERVAL_CHECK, type='int')
# 队列最多存放的任务数
MAX_QUEUE_SIZE = C_proxy.item(item_name='MAX_QUEUE_SIZE', group_name='DEFAULT', default=MAX_QUEUE_SIZE, type='int')
# 网络探测并发线程数
PROCESS_NUM = C_proxy.item(item_name='PROCESS_NUM', group_name='DEFAULT', default=PROCESS_NUM, type='int')
# 抓取配置管理任务的url
URL_WORK_MANAGE_TASK = C_proxy.item(item_name='URL_WORK_MANAGE_TASK', group_name='WORK_MANAGE', default=URL_WORK_MANAGE_TASK, type='str')
# 作业结果上报地址
URL_WORK_MANAGE_REPORT = C_proxy.item(item_name='URL_WORK_MANAGE_REPORT', group_name='WORK_MANAGE', default=URL_WORK_MANAGE_REPORT, type='str')
###################################################################################################