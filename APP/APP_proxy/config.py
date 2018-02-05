#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Proxy的配置文件


###################################################################################################
# Proxy对应的influxdb地址
IP_INFLUXDB = '127.0.0.1'
PORT_INFLUXDB = '8086'
USER_INFLUXDB = 'root'
PASSWORD_INFLUXDB = 'root'
# Durations such as 1h, 90m, 12h, 7d, and 4w, are all supported and mean 1 hour, 90 minutes, 12 hours, 7 day,
# and 4 weeks, respectively. For infinite retention – meaning the data will never be deleted – use ‘INF’
# for duration. The minimum retention period is 1 hour.
DURATION_INFLUXDB = '7d'
REPLICATION_INFLUXDB = '1'             # 一个数据分片存到几台机器上,建议保持默认
# web server地址
WEB_SERVER = '172.16.211.67:80'
# 网络探测任务缓存时长
EXPIRE_NETWORK_DETECT_TASK = '10m'
# 查询网络探测任务的url
URL_NETWORK_DETECT_TASK = 'http://%s/web/network_detect/task/query' % WEB_SERVER
# 抓取属性的名称
NAME_PROPERTY = 'ALL'
# 上报地址
URL_REPORT = 'http://%s/web/reciver?string_name=' % WEB_SERVER
# 检查探测任务的频率(单位: 秒)
INTERVAL_CHECK = 60
# 队列最多存放的任务数
MAX_QUEUE_SIZE = 500
# 网络探测并发线程数
PROCESS_NUM = 100
# 抓取配置管理任务的url
URL_WORK_MANAGE_TASK = 'http://%s/web/configure_manage/work/query_from_asset' % WEB_SERVER
# 作业结果上报地址
URL_WORK_MANAGE_REPORT = 'http://%s/web/reciver?string_name=work_manage' % WEB_SERVER
###################################################################################################
