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
from API.API_agent.config_items import Config
from APP.APP_agent.config import *
###################################################################################################

C_agent = Config()
# 抓取属性的名称
NAME_PROPERTY = C_agent.item(item_name='NAME_PROPERTY', group_name='DEFAULT', default=NAME_PROPERTY, type='str')
# 属性上报地址
URL_REPORT = C_agent.item(item_name='URL_REPORT', group_name='DEFAULT', default=URL_REPORT, type='str')
# 检查探测任务的频率(单位: 秒)
INTERVAL_CHECK = C_agent.item(item_name='INTERVAL_CHECK', group_name='DEFAULT', default=INTERVAL_CHECK, type='int')
# 队列最多存放的任务数
MAX_QUEUE_SIZE = C_agent.item(item_name='MAX_QUEUE_SIZE', group_name='DEFAULT', default=MAX_QUEUE_SIZE, type='int')
# 网络探测并发线程数
PROCESS_NUM = C_agent.item(item_name='PROCESS_NUM', group_name='DEFAULT', default=PROCESS_NUM, type='int')
# 角色
AGENT = C_agent.item(item_name='AGENT', group_name='DEFAULT', default=AGENT, type='eval')
# Agent对应的Proxy地址(不允许配置成127.0.0.0/80,将导致历史信息不可查)
PROXY_SERVER = C_agent.item(item_name='PROXY_SERVER', group_name='DEFAULT', default=PROXY_SERVER, type='str')
# 作为被控制端存在时proxy链接agent的地址
REMOTE_CONTROL_SERVER = C_agent.item(item_name='REMOTE_CONTROL_SERVER', group_name='DEFAULT', default=REMOTE_CONTROL_SERVER, type='str')
# 抓取探测任务的url
URL_NETWORK_DETECT_TASK = C_agent.item(item_name='URL_NETWORK_DETECT_TASK', group_name='NETWORK_DETECT', default=URL_NETWORK_DETECT_TASK, type='str')
# 抓取配置管理任务的url
URL_WORK_MANAGE_TASK = C_agent.item(item_name='URL_WORK_MANAGE_TASK', group_name='WORK_MANAGE', default=URL_WORK_MANAGE_TASK, type='str')
###################################################################################################