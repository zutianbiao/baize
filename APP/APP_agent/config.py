#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Agent的配置文件


###################################################################################################
# Agent对应的Proxy地址(不允许配置成127.0.0.0/80,将导致历史信息不可查)
# PROXY_SERVER = '10.135.28.46:8101'
PROXY_SERVER = '172.18.124.17:8101'
# 作为被控制端存在时proxy链接agent的地址
REMOTE_CONTROL_SERVER = '127.0.0.1:8101'
# 抓取属性的名称
NAME_PROPERTY = 'ALL'
# 属性上报地址
URL_REPORT = 'http://%s/proxy/reciver?string_name=' % PROXY_SERVER
# 检查探测任务的频率(单位: 秒)
INTERVAL_CHECK = 60
# 队列最多存放的任务数
MAX_QUEUE_SIZE = 500
# 网络探测并发线程数
PROCESS_NUM = 100
# 角色
AGENT = True
# 抓取探测任务的url
URL_NETWORK_DETECT_TASK = 'http://%s/proxy/network_detect/task/query' % PROXY_SERVER
# 抓取配置管理任务的url
URL_WORK_MANAGE_TASK = 'http://%s/proxy/configure_manage/work/query_from_asset' % PROXY_SERVER
###################################################################################################