#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django views配置文件


###################################################################################################
import json
from django.http import HttpResponse
from API.API_agent.remote_control import *
from django.views.decorators.csrf import csrf_exempt
from API.API_agent.config_items import Config


@csrf_exempt
def remote_control(request):
    """
    白泽Agent远程控制函数
    参数:
        string_module_name               远程控制模块名称
        string_module_args               模块参数
        string_timeout                   模块执行超时
        string_background                模块是否后台运行[0否1是,默认为0]
    返回值:
        远程控制信息的返回值
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
    string_module_name = request.POST.get('string_module_name', None)
    string_module_args = request.POST.get('string_module_args', None)
    string_timeout = request.POST.get('string_timeout', '30')
    string_background = request.POST.get('string_background', '0')
    sn = request.POST.get('sn', None)
    if sn:
        C_agent = Config()
        SN = C_agent.item(item_name='SN', group_name='ASSET', default=None)
        if sn != SN:
            json_response_data = {
                "success": False,
                "msg": u"验证失败"
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json")

        try:
            json_module_args = eval(string_module_args)
            int_timeout = int(string_timeout)
            int_background = int(string_background)
        except Exception, e:
            try:
                json_module_args = json.loads(str(string_module_args))
                int_timeout = int(string_timeout)
                int_background = int(string_background)
            except Exception, e:
                json_response_data = {
                    "success": False,
                    "msg": u"模块参数不合法"
                }
                return HttpResponse(json.dumps(json_response_data), content_type="application/json")

        try:
            string_function_name = "remote_control_%s" % string_module_name.strip()
            json_response_data = eval(string_function_name)(json_module_args=json_module_args, int_timeout=int_timeout,
                                                            int_background=int_background)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"模块不存在"
            }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json")
    else:
        json_response_data = {
            "success": False,
            "msg": u"验证失败"
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json")


