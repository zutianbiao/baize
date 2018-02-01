#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django views配置文件


###################################################################################################
import json
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fun_active_report(request):
    """ 处理active探测上报 """
    _timestamp_now = time.time() * 1000
    _timestamp = request.GET.get('timestamp', 0)
    if not isinstance(_timestamp, float):
        _timestamp = float(_timestamp)

    if not _timestamp:
        response_data = {'success': False, 'rtt': -1, 'msg': u'请求未携带timestamp参数'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    _rtt = _timestamp_now - _timestamp
    if _rtt < 0:
        _rtt = float(0)
    response_data = {'success': True, 'rtt': _rtt, 'msg': 'client_time=%d,'
                                                          'server_time=%d' % (_timestamp, _timestamp_now)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")