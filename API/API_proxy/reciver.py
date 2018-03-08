#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Proxy的接收器API


###################################################################################################
import json
import time
import urllib
import urllib2
from influxdb import InfluxDBClient
import API.API_proxy.constant as P_C

###################################################################################################


def request(url, method='POST', data={}, timeout=15):
    """ 发起http协议请求 """
    if method == 'POST':
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = json.loads(re)
    else:
        req = urllib2.Request(url=url)
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = json.loads(re)
    return re


def reciver_property(json_data):
    """
    属性接收器
    参数:
        json_data               json属性字典,Demo: {'time': '1494230710','hostname': 'vm-10-135-28-46', 'sn': '111', 'data': {'memory_size': '8.00 GB'}}
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    client = InfluxDBClient(P_C.IP_INFLUXDB, P_C.PORT_INFLUXDB, P_C.USER_INFLUXDB, P_C.PASSWORD_INFLUXDB)
    string_db_name = 'property_list'
    client.create_database(string_db_name)
    string_db_retention_policy = 'auto_delte_1h'
    client.create_retention_policy(string_db_retention_policy, database=string_db_name, duration='1h', replication=P_C.REPLICATION_INFLUXDB, default=True)
    # influxdb存储时间默认是0号时区
    localtime = time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(float(json_data['time']) - 8 * 60 * 60))
    sql_json = [
        {
            "measurement": string_db_name,
            "tags": {
                "hostname": str(json_data['hostname']),
                "sn": str(json_data['sn']),
            },
            "time": localtime,
            "fields": {
                "value": json.dumps(json_data['data'])
            }
        }
    ]
    client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)
    for _key, _value in json_data['data'].items():
        _key = _key.replace('ansible_', '')
        if _key == 'local':
            if not isinstance(_value, dict):
                _value = json.loads(_value)
            for _key2, _value2 in _value.items():
                if not isinstance(_value2, dict):
                    _value2 = json.loads(_value2)
                for _key3, _value3 in _value2.items():
                    string_db_name = "property_%s_%s_%s" % (_key, _key2, _key3)
                    client.create_database(string_db_name)
                    string_db_retention_policy = 'auto_delte_%s' % P_C.DURATION_INFLUXDB
                    client.create_retention_policy(string_db_retention_policy, database=string_db_name,
                                                   duration=P_C.DURATION_INFLUXDB, replication=P_C.REPLICATION_INFLUXDB,
                                                   default=True)
                    sql_json = [
                        {
                            "measurement": string_db_name,
                            "tags": {
                                "hostname": str(json_data['hostname']),
                                "sn": str(json_data['sn']),
                            },
                            "time": localtime,
                            "fields": {
                                "value": str(_value3)
                            }
                        }
                    ]
                    client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)
        if not isinstance(_value, str):
            _value = json.dumps(_value)
        string_db_name = "property_%s" % _key
        client.create_database(string_db_name)
        string_db_retention_policy = 'auto_delte_%s' % P_C.DURATION_INFLUXDB
        client.create_retention_policy(string_db_retention_policy, database=string_db_name, duration=P_C.DURATION_INFLUXDB, replication=P_C.REPLICATION_INFLUXDB, default=True)
        sql_json = [
            {
                "measurement": string_db_name,
                "tags": {
                    "hostname": str(json_data['hostname']),
                    "sn": str(json_data['sn']),
                },
                "time": localtime,
                "fields": {
                    "value": str(_value)
                }
            }
        ]
        client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)

    return {"success": True, "msg": u"成功接收"}


def reciver_network_detect(json_data):
    """
    网络探测接收器
    参数:
        json_data               json属性字典,Demo: {'hostname': 'vm-10-135-28-46', 'sn': '111',
                                                    'data': [{
                                                         "time": "1494230710.000000",
                                                        "task_id": 0,
                                                        "source": 0,   # id编号
                                                        "target": '1.1.1.1',
                                                        "steps": 300,
                                                        "uri": '',
                                                        "timeout_total": 30,
                                                        "timeout_conn": 3,
                                                        "timeout_dns": 3,
                                                        "type": "curl",
                                                        "success": True,
                                                        "time_conn": 0.01,
                                                        "time_total": 1.10,
                                                        "file_size": 100000,
                                                        "speed": 100000
                                                    }]}
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    client = InfluxDBClient(P_C.IP_INFLUXDB, P_C.PORT_INFLUXDB, P_C.USER_INFLUXDB, P_C.PASSWORD_INFLUXDB)
    string_db_name = 'network_detect_list'
    client.create_database(string_db_name)
    string_db_retention_policy = 'auto_delte_1h'
    client.create_retention_policy(string_db_retention_policy, database=string_db_name, duration='1h', replication=P_C.REPLICATION_INFLUXDB, default=True)
    # influxdb存储时间默认是0号时区
    localtime = time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(time.time() - 8 * 60 * 60))
    sql_json = [
        {
            "measurement": string_db_name,
            "tags": {
                "hostname": str(json_data['hostname']),
                "sn": str(json_data['sn']),
            },
            "time": localtime,
            "fields": {
                "value": json.dumps(json_data['data'])
            }
        }
    ]
    client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)

    for result in json_data['data']:
        if isinstance(result, str):
            result = json.loads(result)
        string_db_name = "network_detect_%s" % result['type']
        client.create_database(string_db_name)
        string_db_retention_policy = 'auto_delte_%s' % P_C.DURATION_INFLUXDB
        client.create_retention_policy(string_db_retention_policy, database=string_db_name, duration=P_C.DURATION_INFLUXDB, replication=P_C.REPLICATION_INFLUXDB, default=True)
        if result['type'] == 'curl':
            sql_json = [
                {
                    "measurement": string_db_name,
                    "tags": {
                        "hostname": str(json_data['hostname']),
                        "sn": str(json_data['sn']),
                        "task_id": str(result['task_id']),
                        "source": str(result['source']),
                        "target": str(result['target']),
                        "steps": str(result['steps']),
                        "timeout_total": str(result['timeout_total']),
                        "timeout_conn": str(result['timeout_conn']),
                        "timeout_dns": str(result['timeout_dns']),
                        "uri": str(result['uri']),
                        "modtime": str(result['modtime']),
                    },
                    "time": time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(float(result['time']) - 8 * 60 * 60)),
                    "fields": {
                        "success": result['success'],
                        "time_conn": str(result['time_conn']),
                        "time_total": str(result['time_total']),
                        "file_size": str(result['file_size']),
                        "speed": str(result['speed']),
                    }
                }
            ]
        elif result['type'] == 'ping':
            sql_json = [
                {
                    "measurement": string_db_name,
                    "tags": {
                        "hostname": str(json_data['hostname']),
                        "sn": str(json_data['sn']),
                        "task_id": str(result['task_id']),
                        "source": str(result['source']),
                        "target": str(result['target']),
                        "steps": str(result['steps']),
                        "num": str(result['num']),
                        "interval": str(result['interval']),
                        "timeout": str(result['timeout']),
                        "size": str(result['size']),
                        "modtime": str(result['modtime']),
                    },
                    "time": time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(float(result['time']) - 8 * 60 * 60)),
                    "fields": {
                        "success": str(result['success']),
                        "lost_rate": str(result['lost_rate']),
                        "rtt": str(result['rtt']),
                    }
                }
            ]
        elif result['type'] == 'traceroute':
            sql_json = [
                {
                    "measurement": string_db_name,
                    "tags": {
                        "hostname": str(json_data['hostname']),
                        "sn": str(json_data['sn']),
                        "task_id": str(result['task_id']),
                        "source": str(result['source']),
                        "target": str(result['target']),
                        "steps": str(result['steps']),
                        "num": str(result['num']),
                        "timeout": str(result['timeout']),
                        "modtime": str(result['modtime']),
                    },
                    "time": time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(float(result['time']) - 8 * 60 * 60)),
                    "fields": {
                        "success": str(result['success']),
                        "data": str(result['data']),
                    }
                }
            ]
        client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)

    return {"success": True, "msg": u"成功接收"}


def reciver_work_manage(json_data):
    """
    作业结果接收器
    参数:
        json_data               json属性字典,Demo: {'hostname': 'vm-10-135-28-46', 'sn': '111', "work_id": 3, "type": "test", "data": [{"job": {"type":"command","id":"1","ignore_error":false}, "data": "xxxx", "msg": "dsdsds", "success": True}]
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 成功返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    return request(P_C.URL_WORK_MANAGE_REPORT, data=json_data)
