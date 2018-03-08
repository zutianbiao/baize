#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Proxy的接收器API


###################################################################################################
import json
import datetime
from APP.APP_web.models import Property, Asset, Property_Template, Asset_Data, Detect_Role, Ping_Detect, \
    Traceroute_Detect, Curl_Detect, Configure_Manage_Work_Result, Configure_Manage_Work_Result_Data, \
    Configure_Manage_Work, Configure_Manage_Work_Tag_Data


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
    try:
        _asset = Asset.objects.get(name=json_data['hostname'], sn=json_data['sn'])
    except Exception, e:
        _asset = Asset(name=json_data['hostname'], sn=json_data['sn'], desc=json_data['hostname'])
        _asset.save()

    if not isinstance(json_data['data'], dict):
        json_data['data'] = json.loads(json_data['data'])

    for _key, _value in json_data['data'].items():
        _key = _key.replace('ansible_', '')
        if _key == 'local':
            if not isinstance(_value, dict):
                _value = json.loads(_value)
            for _key2, _value2 in _value.items():
                if not isinstance(_value2, dict):
                    _value2 = json.loads(_value2)
                for _key3, _value3 in _value2.items():
                    _key_final = "%s_%s_%s" % (_key, _key2, _key3)
                    try:
                        _property_template = Property_Template.objects.get(name=_key_final)
                    except Exception, e:
                        _property_template = Property_Template(name=_key_final, desc=_key_final, type='text', steps=5,
                                                               reciver='default')
                        _property_template.save()
                    try:
                        _property = _asset.property.filter(property_template=_property_template).order_by('modtime')[0]
                        if _property.value != _value3:
                            # 属性覆盖
                            if _property_template.save_method == 0:
                                _property.value = _value3
                                _property.save()
                            else:
                                # 属性追加
                                _property = Property(property_template=_property_template, value=_value3)
                                _property.save()
                                _asset_data = Asset_Data(property=_property, asset=_asset)
                                _asset_data.save()
                    except Exception, e:
                        _property = Property(property_template=_property_template, value=_value3)
                        _property.save()
                        _asset_data = Asset_Data(property=_property, asset=_asset)
                        _asset_data.save()
        if not isinstance(_value, str):
            _value = json.dumps(_value)
        try:
            _property_template = Property_Template.objects.get(name=_key)
        except Exception, e:
            _property_template = Property_Template(name=_key, desc=_key, type='text', steps=5, reciver='default')
            _property_template.save()
        try:
            _property = _asset.property.filter(property_template=_property_template).order_by('modtime')[0]
            if _property.value != _value:
                # 属性覆盖
                if _property_template.save_method == 0:
                    _property.value = _value
                    _property.save()
                else:
                # 属性追加
                    _property = Property(property_template=_property_template, value=_value)
                    _property.save()
                    _asset_data = Asset_Data(property=_property, asset=_asset)
                    _asset_data.save()
        except Exception, e:
            _property = Property(property_template=_property_template, value=_value)
            _property.save()
            _asset_data = Asset_Data(property=_property, asset=_asset)
            _asset_data.save()

    return {"success": True, "msg": u"成功接收"}


def reciver_network_detect(json_data):
    """
    网络探测接收器
    参数:
        json_data               json属性字典,Demo: {"modtime": 1496636583.0, "timeout_conn": 3, "type": "curl", "target": "211.154.226.143", "target_id": 1, "task_id": 1, "time_conn": 0.001151, "file_size": 169.0, "uri": "", "timeout_total": 300, "source": 1, "timeout_dns": 3, "steps": 300, "time": 1496800322.388059, "success": true, "speed": 71068.0, "time_total": 0.002378}
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
    if json_data['type'] == 'ping':
        try:
            ping_detect = Ping_Detect.objects.get(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'])
            ping_detect.steps = json_data['steps']
            ping_detect.num = json_data['num']
            ping_detect.interval = json_data['interval']
            ping_detect.timeout = json_data['timeout']
            ping_detect.size = json_data['size']
            ping_detect.success = json_data['success']
            ping_detect.lost_rate = json_data['lost_rate']
            ping_detect.rtt = json_data['rtt']
            ping_detect.modtime = datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60)
            ping_detect.save()
        except Exception, e:
            # 如果任务不存在那么直接放弃探测结果
            pass
            # ping_detect = Ping_Detect(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'], steps=json_data['steps'], num=json_data['num'], interval=json_data['interval'], timeout=json_data['timeout'], size=json_data['size'], success=json_data['success'], lost_rate=json_data['lost_rate'], rtt=json_data['rtt'], modtime=datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60))
        # ping_detect.save()
    elif json_data['type'] == 'traceroute':
        try:
            traceroute_detect = Traceroute_Detect.objects.get(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'])
            traceroute_detect.steps = json_data['steps']
            traceroute_detect.num = json_data['num']
            traceroute_detect.timeout = json_data['timeout']
            traceroute_detect.success = json_data['success']
            traceroute_detect.data = json_data['data']
            traceroute_detect.modtime = datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60)
            traceroute_detect.save()
        except Exception, e:
            pass
            # traceroute_detect = Traceroute_Detect(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'], steps=json_data['steps'], num=json_data['num'], timeout=json_data['timeout'], success=json_data['success'], data=json_data['data'], modtime=datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60))
        # traceroute_detect.save()
    if json_data['type'] == 'curl':
        try:
            curl_detect = Curl_Detect.objects.get(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'], uri=json_data['uri'])
            curl_detect.steps = json_data['steps']
            curl_detect.timeout_total = json_data['timeout_total']
            curl_detect.timeout_conn = json_data['timeout_conn']
            curl_detect.timeout_dns = json_data['timeout_dns']
            curl_detect.success = json_data['success']
            curl_detect.time_conn = json_data['time_conn']
            curl_detect.time_total = json_data['time_total']
            curl_detect.file_size = json_data['file_size']
            curl_detect.speed = json_data['speed']
            curl_detect.modtime = datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60)
            curl_detect.save()
        except Exception, e:
            pass
            # curl_detect = Curl_Detect(task_id=json_data['task_id'], source_id=json_data['source'], target_id=json_data['target_id'], steps=json_data['steps'], uri=json_data['uri'], timeout_total=json_data['timeout_total'], timeout_conn=json_data['timeout_conn'], timeout_dns=json_data['timeout_dns'], success=json_data['success'], time_conn=json_data['time_conn'], time_total=json_data['time_total'], file_size=json_data['file_size'], speed=json_data['speed'], modtime=datetime.datetime.fromtimestamp(json_data['modtime'] - 8 * 60 * 60))
        # curl_detect.save()

    return {"success": True, "msg": u"成功接收"}


def reciver_work_manage(json_data):
    """
    作业结果接收器
    参数:
        json_data               json属性字典,Demo: {
                                                  "hostname": "localhost",
                                                  "sn": "111",
                                                  "data": [
                                                      {
                                                           "id": 1,
                                                           "name_cn": '测试作业',
                                                           "name_en": 'test',
                                                           "desc": '测试作业',
                                                           "jobs": list_jobs,
                                                           "timeout": timeout,
                                                           "sync": sync,
                                                           "type": "online",
                                                           "success": True,
                                                           "result": list_result,
                                                           "time": 1496636583.0
                                                       },
                                                  ]
                                             }

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

    try:
        _asset = Asset.objects.get(name=json_data['hostname'], sn=json_data['sn'])
    except Exception, e:
        _asset = Asset(name=json_data['hostname'], sn=json_data['sn'], desc=json_data['hostname'])
        _asset.save()

    if not isinstance(json_data['data'], list):
        json_data['data'] = json.loads(json_data['data'])

    for _jdd in json_data['data']:
        modtime = datetime.datetime.fromtimestamp(json_data['time'] - 8 * 60 * 60)

        try:
            _work_result_data = Configure_Manage_Work_Result_Data.objects.get(work_id=_jdd['id'], asset=_asset)
        except Exception, e:
            _work_result = Configure_Manage_Work_Result(data=_jdd['result'], jobs=_jdd['jobs'], success=_jdd['success'], type=_jdd['type'], modtime=modtime)
            _work_result.save()
            _work_result_data = Configure_Manage_Work_Result_Data(work_id=_jdd['id'], result=_work_result, asset=_asset)
            _work_result_data.save()

    return {"success": True, "msg": u"成功接收"}