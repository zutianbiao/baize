#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django views配置文件


###################################################################################################
import json
import urllib
import urllib2
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from API.API_proxy.reciver import *
from config import *
from influxdb import InfluxDBClient


@csrf_exempt
def reciver(request):
    """
    白泽Proxy接收器接入函数
    参数:
        string_name                      GET参数,接收器名称
        json信息                         POST文本,Demo: {'time': '1494230710','hostname': 'vm-10-135-28-46', 'sn': '111', 'data': {'memory_size': '8.00 GB'}}
    返回值:
        接收器接收消息的成功失败信息
        执行成功：
            {
                "success": True,
                "msg": "模块返回值"
            }
        执行失败：
            {
                "success": False,
                "msg": "模块异常返回值"
            }
    """
    string_reciver_name = request.GET.get('string_name', None)
    time = request.POST.get('time', None)
    hostname = request.POST.get('hostname', None)
    sn = request.POST.get('sn', None)
    data = eval(request.POST.get('data', None))
    json_info = {'time': time, 'hostname': hostname, 'sn': sn, 'data': data}
    try:
        string_function_name = "reciver_%s" % string_reciver_name.strip()
        json_response_data = eval(string_function_name)(json_info)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"模块不存在"
        }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json")


def do_request(url, method='POST', data={}, timeout=15):
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


@csrf_exempt
def network_detect_task_query(request):
    """ 查询探测任务 """
    hostname = request.POST.get('hostname', '')
    sn = request.POST.get('sn', '')
    if not sn or not hostname:
        response_data = {
            'success': False,
            'msg': u"未传递主机名和sn号"
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    client = InfluxDBClient(IP_INFLUXDB, PORT_INFLUXDB, USER_INFLUXDB, PASSWORD_INFLUXDB)
    string_db_name = 'network_detect_task'
    client.create_database(string_db_name)
    string_db_retention_policy = 'auto_delte_1d'
    client.create_retention_policy(string_db_retention_policy, database=string_db_name, duration='1d', replication=REPLICATION_INFLUXDB, default=True)
    sql = """select * from %s where time>now() - %s and hostname='%s' and sn='%s' limit 1;""" % (string_db_name, EXPIRE_NETWORK_DETECT_TASK, hostname, sn)
    sql_result = client.query(sql, database=string_db_name)
    list_task = list(sql_result.get_points())
    if list_task:
        response_data = list_task[0]['data']
        if isinstance(response_data, str):
            response_data = json.loads(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = {
            "hostname": hostname,
            "sn": sn
        }
        response_data = do_request(URL_NETWORK_DETECT_TASK, data=data)
        if response_data['success']:
            localtime = time.strftime('%Y-%m-%dT%H:%M:00Z', time.localtime(float(time.time()) - 8 * 60 * 60))
            sql_json = [
                {
                    "measurement": string_db_name,
                    "tags": {
                        "hostname": hostname,
                        "sn": sn,
                    },
                    "time": localtime,
                    "fields": {
                        "data": json.dumps(response_data)
                    }
                }
            ]
            client.write_points(sql_json, database=string_db_name, retention_policy=string_db_retention_policy)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {
                'success': False,
                'msg': u"获取探测任务失败"
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def network_detect_task_query_history(request):
    """查询历史探测任务数据的API"""
    source = request.POST.get('source', None)
    target = request.POST.get('target', None)
    db = request.POST.get('db', None)
    item = request.POST.get('item', None)
    period = request.POST.get('period', None)
    task_id = request.POST.get('task_id', None)
    if source:
        sql = """select %s,time from %s where time> now() - %s and source='%s' and target='%s' and task_id='%s' order by time;""" % (item, db, period, source, target, task_id)
        try:
            client = InfluxDBClient(IP_INFLUXDB, PORT_INFLUXDB, USER_INFLUXDB, PASSWORD_INFLUXDB)
            sql_result = client.query(sql, database=db)
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"探测源Proxy Server查询失败",
                'data': []
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        list_result = list(sql_result.get_points())
        _lt = list()
        for i in list_result:
            time_now_unix = (time.mktime(datetime.datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:00Z").timetuple()) + 8 * 60 * 60) * 1000
            try:
                _item = float(i[item])
            except Exception, e:
                _item = 0.00
            _lt.append([time_now_unix, _item])
        response_data = {
            'success': True,
            'msg': u"查询历史信息成功",
            'data': _lt
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {
            'success': False,
            'msg': u"参数不合法",
            'data': []
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def remote_control(request):
    """远程控制"""
    string_module_name = request.POST.get('string_module_name', None)
    string_module_args = request.POST.get('string_module_args', None)
    string_timeout = request.POST.get('string_timeout', '30')
    string_background = request.POST.get('string_background', '0')
    string_agents = request.POST.get('string_agents', None)
    sn = request.POST.get('sn', None)
    try:
        list_agents = eval(string_agents)
    except Exception, e:
        try:
            list_agents = json.loads(str(string_agents))
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"string_agents参数不合法"
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json")
    json_response_data = {
        "success": True,
        "msg": u"远程控制完成",
        "data": []
    }
    for agent in list_agents:
        url = "http://%s/agent/remote_control" % agent
        json_post_data = {
            "string_module_name": string_module_name,
            "string_module_args": string_module_args,
            "string_timeout": string_timeout,
            "string_background": string_background,
            "sn": sn
        }
        data = do_request(url, data=json_post_data)
        _dt = {
            "agent": agent,
            "data": data
        }
        json_response_data['data'].append(_dt)

    return HttpResponse(json.dumps(json_response_data), content_type="application/json")


@csrf_exempt
def configure_manage_work_query_from_asset(request):
    """ 单资产查询测试作业 """
    hostname = request.POST.get('hostname', '')
    sn = request.POST.get('sn', '')
    if not sn or not hostname:
        response_data = {
            'success': False,
            'msg': u"未传递主机名和sn号",
            'data': []
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    data = {
        "hostname": hostname,
        "sn": sn
    }
    # response_data = do_request(P_C.URL_WORK_MANAGE_TASK, data=data)
    data = urllib.urlencode(data)
    req = urllib2.Request(url=P_C.URL_WORK_MANAGE_TASK, data=data)
    url_open = urllib2.urlopen(req, timeout=15)
    response_data = url_open.read()
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
def asset_manage_property_query_history(request):
    hostname = request.POST.get('hostname', '')
    sn = request.POST.get('sn', '')
    property_name = request.POST.get('property_name', '')
    time_start = request.POST.get('time_start', None)
    time_end = request.POST.get('time_end', None)
    if not sn or not hostname or not property_name or not time_start or not time_end:
        response_data = {
            'success': False,
            'msg': u"参数不合法",
            'data': []
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    time_start = time.strftime("%Y-%m-%dT%H:%M:00Z",time.localtime(time.mktime(time.strptime(time_start, "%Y-%m-%d %H:%M")) - 8 * 60 * 60))
    time_end = time.strftime("%Y-%m-%dT%H:%M:00Z",time.localtime(time.mktime(time.strptime(time_end, "%Y-%m-%d %H:%M")) - 8 * 60 * 60))
    db = "property"
    sql = """select value,time from property_%s where time>= '%s' and time <= '%s' order by time;""" % (property_name, time_start, time_end)
    try:
        client = InfluxDBClient(IP_INFLUXDB, PORT_INFLUXDB, USER_INFLUXDB, PASSWORD_INFLUXDB)
        sql_result = client.query(sql, database=db)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"Proxy Server查询失败",
            'data': None
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    list_result = list(sql_result.get_points())
    _lt = list()
    for i in list_result:
        time_now_unix = (time.mktime(datetime.datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:00Z").timetuple()) + 8 * 60 * 60) * 1000
        try:
            _value = float(i['value'])
        except Exception, e:
            _value = 0.00
        _lt.append([time_now_unix, _value])
    response_data = {
        'success': True,
        'msg': u"查询成功",
        'data': _lt
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")