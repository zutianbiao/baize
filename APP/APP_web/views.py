#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django views配置文件


###################################################################################################
import os
import json
import logging
import hashlib
import base64
import time
import urllib
import urllib2
import baize.settings as C
from ftplib import FTP
from urlparse import urlparse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponseRedirect
from API.API_web.config_items import Config
from API.API_web.reciver import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from API.API_web.generate_password import fun_generate_password
from django.core.mail import send_mass_mail
from baize.settings import EMAIL_HOST_USER, ADMIN_EMAIL
from django.contrib.auth.decorators import login_required
from models import Asset, Detect_Role, Geo, Isp, Detect_Task, Ping_Detect, Traceroute_Detect, Curl_Detect, \
    Remote_Control_Command, Remote_Control_Script, Remote_Control_Copy, Asset_Tag, Asset_Tag_Data, \
    Business_Tree, Configure_Manage_Work, Configure_Manage_Work_Tag_Data, Configure_Manage_Task, \
    Configure_Manage_Task_Data, Authority_Url, Authority_Bussiness, Bussiness, Bussiness_Btn


def authority_url(func):
    def inner(request, *args, **kwargs):
        try:
            superuser = request.user.is_superuser
        except Exception, e:
            superuser = True
        if not superuser:
            try:
                list_authority = Authority_Url.objects.filter(url__contains=request.path, user=request.user)
            except Exception, e:
                list_authority = []

            if not list_authority:
                http_accept = request.META.get('HTTP_ACCEPT', '')
                if 'json' not in http_accept:
                    return fun_403(request, *args, **kwargs)
                else:
                    response_data = {
                        "success": False,
                        "msg": u"url权限不足,请联系管理员"
                    }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
        return func(request, *args, **kwargs)

    return inner


def baize_register(username, email):
    C_web = Config()
    length = int(C_web.item(item_name='LENGTH_PASSWORD_RANDOM', group_name='PASSWORD', default=u"""8"""))
    _secret_method = C_web.item(item_name='SECRET_METHOD', group_name='MASTER', default=u"""pbkdf2_sha256""")
    _password = fun_generate_password(length=length)
    try:
        _secret_password = make_password(_password, None, _secret_method)
    except Exception, e:
        logger = logging.getLogger('log_file')
        logger.error(e)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.error(e)
        _secret_password = _password
    message1 = (u"【Baize】注册成功", u"恭喜您,注册白泽系统成功,您的账号: %s, 密码: %s" % (username, _password), EMAIL_HOST_USER, [email, ])
    message2 = (u"【Baize】注册提醒", u"%s注册成功,邮箱: %s, 密码: %s" % (username, email, _password), EMAIL_HOST_USER, [ADMIN_EMAIL, ])
    try:
        user = User.objects.filter(username=username, email=email)
    except Exception, e:
        user = None
    if user:
        log_message = u"%s已经存在,邮箱: %s" % (username, email)
        logger = logging.getLogger('log_file')
        logger.info(log_message)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.info(log_message)
        _re = {
            "success": False,
            "msg": u"您注册的邮箱已经存在"
        }
    else:
        user = User(username=username, email=email, password=_secret_password)
        try:
            _res = send_mass_mail((message1, message2), fail_silently=False)
        except Exception, e:
            logger = logging.getLogger('log_file')
            logger.error(e)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.error(e)
            _res = 0
        if _res >= 2:
            user.save()
            log_message = u"%s注册成功,邮箱: %s" % (username, email)
            logger = logging.getLogger('log_file')
            logger.info(log_message)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.info(log_message)
            _re = {
                "success": True,
                "msg": u"注册成功"
            }
        elif _res == 0:
            log_message = u"注册失败,邮箱%s不存在" % email
            logger = logging.getLogger('log_file')
            logger.info(log_message)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.info(log_message)
            _re = {
                "success": False,
                "msg": u"您注册的邮箱不存在"
            }
        else:
            log_message = u"%s注册失败,邮箱: %s" % (username, email)
            logger = logging.getLogger('log_file')
            logger.info(log_message)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.info(log_message)
            _re = {
                "success": False,
                "msg": u"您注册的邮箱不存在"
            }
    return _re


@csrf_exempt
def register(request):
    C_web = Config()
    argv_local = dict()
    argv_local['BODY_BG'] = 'gray-bg'
    if request.method == 'GET':
        argv_local["DEFAULT"] = {
            "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"Baize"),
            "MSG_WELCOME_REGISTER": C_web.item(item_name='MSG_WELCOME_REGISTER', group_name='DEFAULT',
                                               default=u"Register to Baize"),
            "MSG_REGISTER": C_web.item(item_name='MSG_REGISTER', group_name='DEFAULT',
                                       default=u"""<div class="text-normal">Create account to see it in action.</div>"""),
            "MSG_ACCOUNT_HAVE": C_web.item(item_name='MSG_ACCOUNT_HAVE', group_name='DEFAULT',
                                           default=u"""Already have an account?"""),
            "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT', default=u"""© 联通支付技术部运行维护中心 2017"""),
        }
        return render_to_response('login/register.html', argv_local)
    else:
        username = request.POST['username']
        email = request.POST['email']
        _re = baize_register(username, email)
        if _re['msg'] == u'注册成功':
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT',
                                          default=u"""Welcome to Baize"""),
                "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT',
                                        default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
                "MSG_LOGIN": C_web.item(item_name='MSG_LOGIN_SUCCESS', group_name='DEFAULT',
                                        default=u"""<div class="text-normal">Login in. To see it in action.</div>"""),
                "MSG_FORGOT_PASSWORD": C_web.item(item_name='MSG_FORGOT_PASSWORD', group_name='DEFAULT',
                                                  default=u"""Forgot password?"""),
                "MSG_ACCOUNT_NOHAVE": C_web.item(item_name='MSG_ACCOUNT_NOHAVE', group_name='DEFAULT',
                                                 default=u"""Do not have an account?"""),
                "MSG_CREATE_ACCOUNT": C_web.item(item_name='MSG_CREATE_ACCOUNT', group_name='DEFAULT',
                                                 default=u"""Create an account"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/login.html', argv_local)
        elif _re['msg'] == u'您注册的邮箱已经存在':
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT',
                                          default=u"""Welcome to Baize"""),
                "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT',
                                        default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
                "MSG_LOGIN": C_web.item(item_name='MSG_REGISTER_CONFLICT', group_name='DEFAULT',
                                        default=u"""<div class="text-danger">用户名已经存在</div>"""),
                "MSG_FORGOT_PASSWORD": C_web.item(item_name='MSG_FORGOT_PASSWORD', group_name='DEFAULT',
                                                  default=u"""Forgot password?"""),
                "MSG_ACCOUNT_NOHAVE": C_web.item(item_name='MSG_ACCOUNT_NOHAVE', group_name='DEFAULT',
                                                 default=u"""Do not have an account?"""),
                "MSG_CREATE_ACCOUNT": C_web.item(item_name='MSG_CREATE_ACCOUNT', group_name='DEFAULT',
                                                 default=u"""Create an account"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/login.html', argv_local)
        else:
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_WELCOME_REGISTER": C_web.item(item_name='MSG_WELCOME_REGISTER', group_name='DEFAULT',
                                                   default=u"""Register to Baize"""),
                "MSG_REGISTER": C_web.item(item_name='MSG_REGISTER_ERROR', group_name='DEFAULT',
                                           default=u"""<div class="text-danger">注册使用的邮箱不存在</div>"""),
                "MSG_ACCOUNT_HAVE": C_web.item(item_name='MSG_ACCOUNT_HAVE', group_name='DEFAULT',
                                               default=u"""Already have an account?"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/register.html', argv_local)


@login_required
@csrf_exempt
def reset(request):
    C_web = Config()
    argv_local = dict()
    if request.method == 'GET':
        argv_local["DEFAULT"] = {
            "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
            "MSG_RESET": C_web.item(item_name='MSG_RESET', group_name='DEFAULT',
                                    default=u"""Enter your email address and your password will be reset and emailed to you."""),
            "MSG_RESET_TITLE": C_web.item(item_name='MSG_RESET_TITLE', group_name='DEFAULT',
                                          default=u"""Forgot password"""),
            "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT', default=u"""© 联通支付技术部运行维护中心 2017"""),
        }
        return render_to_response('login/reset.html', argv_local)
    else:
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except Exception, e:
            logger = logging.getLogger('log_file')
            logger.error(e)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.error(e)
            user = None
        if user == request.user:
            username = user.username
            length = int(C_web.item(item_name='LENGTH_PASSWORD_RANDOM', group_name='PASSWORD', default=u"""8"""))
            _secret_method = C_web.item(item_name='SECRET_METHOD', group_name='MASTER', default=u"""pbkdf2_sha256""")
            _password = fun_generate_password(length=length)
            try:
                _secret_password = make_password(_password, None, _secret_method)
                user.password = _secret_password
            except Exception, e:
                logger = logging.getLogger('log_file')
                logger.error(e)
                if C.LOG_SCREEN == 'ON':
                    logger = logging.getLogger('log_screen')
                    logger.error(e)
            message1 = (u"【Baize】重置密码成功", u"重置密码成功,您的账号: %s, 密码: %s" % (username, _password), EMAIL_HOST_USER, [email, ])
            message2 = (u"【Baize】重置密码提醒", u"%s重置密码成功,邮箱: %s, 密码: %s" % (username, email, _password), EMAIL_HOST_USER, [ADMIN_EMAIL, ])
            _res = send_mass_mail((message1, message2), fail_silently=False)
            user.save()
            if _res >= 2:
                _re = {
                    "success": False,
                    "msg": u"重置密码成功"
                }
            else:
                _re = {
                    "success": False,
                    "msg": u"邮箱通信异常"
                }
        else:
            _re = {
                "success": False,
                "msg": u"该邮箱不存在"
            }
        if _re['msg'] == u'重置密码成功':
            auth.logout(request)
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT',
                                          default=u"""Welcome to Baize"""),
                "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT',
                                        default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
                "MSG_LOGIN": C_web.item(item_name='MSG_RESET_SUCCESS', group_name='DEFAULT',
                                        default=u"""<div class="text-primary">重置密码成功,请使用邮箱中的密码登录</div>"""),
                "MSG_FORGOT_PASSWORD": C_web.item(item_name='MSG_FORGOT_PASSWORD', group_name='DEFAULT',
                                                  default=u"""Forgot password?"""),
                "MSG_ACCOUNT_NOHAVE": C_web.item(item_name='MSG_ACCOUNT_NOHAVE', group_name='DEFAULT',
                                                 default=u"""Do not have an account?"""),
                "MSG_CREATE_ACCOUNT": C_web.item(item_name='MSG_CREATE_ACCOUNT', group_name='DEFAULT',
                                                 default=u"""Create an account"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/login.html', argv_local)
        else:
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_RESET": C_web.item(item_name='MSG_RESET_NOUSER', group_name='DEFAULT',
                                        default=u"""<div class="text-danger">该邮箱不存在</div>"""),
                "MSG_RESET_TITLE": C_web.item(item_name='MSG_RESET_TITLE', group_name='DEFAULT',
                                              default=u"""Forgot password"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/reset.html', argv_local)


@csrf_exempt
def logout(request):
    """ 退出 """
    log_message = u'%s 退出' % str(request.user)
    try:
        auth.logout(request)
        logger = logging.getLogger('log_file')
        logger.info(log_message)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.info(log_message)
        return HttpResponseRedirect("/web/index")
    except Exception, e:
        logger = logging.getLogger('log_file')
        logger.error(e)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.error(e)
        response_data = {
            "success": False,
            "msg": u"退出失败"
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def login(request):
    """
    白泽Web登录页
    """
    C_web = Config()
    argv_local = dict()
    argv_local['BODY_BG'] = 'gray-bg'
    _username = request.POST.get('username', '')
    _password = request.POST.get('password', '')
    if request.method == 'GET':
        argv_local["DEFAULT"] = {
            "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
            "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT', default=u"""Welcome to Baize"""),
            "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT',
                                    default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
            "MSG_LOGIN": C_web.item(item_name='MSG_LOGIN', group_name='DEFAULT',
                                    default=u"""<div class="text-normal">Login in. To see it in action.</div>"""),
            "MSG_FORGOT_PASSWORD": C_web.item(item_name='MSG_FORGOT_PASSWORD', group_name='DEFAULT',
                                              default=u"""Forgot password?"""),
            "MSG_ACCOUNT_NOHAVE": C_web.item(item_name='MSG_ACCOUNT_NOHAVE', group_name='DEFAULT',
                                             default=u"""Do not have an account?"""),
            "MSG_CREATE_ACCOUNT": C_web.item(item_name='MSG_CREATE_ACCOUNT', group_name='DEFAULT',
                                             default=u"""Create an account"""),
            "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT', default=u"""© 联通支付技术部运行维护中心 2017"""),
        }
        return render_to_response('login/login.html', argv_local)
    else:
        _next = request.GET.get('next', '/web/index')
        user = authenticate(username=_username, password=_password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = _username
            login_timeout = int(C_web.item(item_name='LOGIN_TIMEOUT', group_name='TIMEOUT', default=u"""86400"""))
            request.session.set_expiry(login_timeout)
            argv_local.update(csrf(request))
            return HttpResponseRedirect(_next, argv_local)
        else:
            argv_local["DEFAULT"] = {
                "WEB_TITLE": C_web.item(item_name='WEB_TITLE', group_name='DEFAULT', default=u"""Baize"""),
                "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT',
                                          default=u"""Welcome to Baize"""),
                "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT',
                                        default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
                "MSG_LOGIN": C_web.item(item_name='MSG_LOGIN_FAILED', group_name='DEFAULT',
                                        default=u"""<div class="text-danger">用户名密码错误,无法登录</div>"""),
                "MSG_FORGOT_PASSWORD": C_web.item(item_name='MSG_FORGOT_PASSWORD', group_name='DEFAULT',
                                                  default=u"""Forgot password?"""),
                "MSG_ACCOUNT_NOHAVE": C_web.item(item_name='MSG_ACCOUNT_NOHAVE', group_name='DEFAULT',
                                                 default=u"""Do not have an account?"""),
                "MSG_CREATE_ACCOUNT": C_web.item(item_name='MSG_CREATE_ACCOUNT', group_name='DEFAULT',
                                                 default=u"""Create an account"""),
                "WEB_FOOTER": C_web.item(item_name='WEB_FOOTER', group_name='DEFAULT',
                                         default=u"""© 联通支付技术部运行维护中心 2017"""),
            }
            return render_to_response('login/login.html', argv_local)


@login_required
def index(request):
    """
    白泽Web主页
    """
    C_web = Config()
    argv_local = dict()
    argv_local["DEFAULT"] = {
        "MSG_WELCOME": C_web.item(item_name='MSG_WELCOME', group_name='DEFAULT', default=u"""Welcome to Baize"""),
        "MSG_USAGE": C_web.item(item_name='MSG_USAGE', group_name='DEFAULT', default=u"""打造通用型自动化运维平台.助力传统运维向Devops转型"""),
    }
    argv_local['USER'] = request.user.username
    return render_to_response('login/index.html', argv_local)


@login_required
@csrf_exempt
def product_center(request):
    """
    白泽Web产品中心
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    return render_to_response('product_center/product_center.html', argv_local)


@login_required
@csrf_exempt
def asset_manage(request):
    """
    白泽Web 资产管理产品
    """
    argv_local = dict()
    argv_local['USER'] = request.user.username
    return render_to_response('asset_manage/asset_manage.html', argv_local)


@login_required
@csrf_exempt
def asset_manage_index(request):
    """
    白泽Web 资产管理产品 主页
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    dict_asset_id_to_tag_name = {}
    try:
        asset_tag_data = Asset_Tag_Data.objects.all()
        for atd in asset_tag_data:
            if str(atd.asset.id) in dict_asset_id_to_tag_name:
                if not atd.asset_tag.ontree:
                    dict_asset_id_to_tag_name[str(atd.asset.id)].append(atd.asset_tag.name)
            else:
                if not atd.asset_tag.ontree:
                    dict_asset_id_to_tag_name[str(atd.asset.id)] = [atd.asset_tag.name]
                else:
                    dict_asset_id_to_tag_name[str(atd.asset.id)] = []
    except Exception, e:
        pass

    _asset = Asset.objects.all()
    list_property = list()
    _dt = dict()
    for _at in _asset:
        _dt['sn'] = _at.sn
        _dt['hostname'] = _at.name
        _dt['id'] = _at.id
        if str(_at.id) in dict_asset_id_to_tag_name:
            _dt['tag_list'] = dict_asset_id_to_tag_name[str(_at.id)]
        else:
            _dt['tag_list'] = []
        list_property_now = _at.property.filter(property_template_id='all_ipv4_addresses')
        for _lpn in list_property_now:
            try:
                _value = json.loads(_lpn.value)
            except Exception, e:
                _value = _lpn.value
            _dt[str(_lpn.property_template)] = _value
        list_property.append(_dt)
        _dt = dict()
    argv_local['LIST_PROPERTY'] = list_property
    list_tag = list()
    _asset_tag = Asset_Tag.objects.filter(ontree=False)[:10]
    _dt = dict()
    for _at in _asset_tag:
        _dt['id'] = _at.id
        _dt['name'] = _at.name
        list_tag.append(_dt)
        _dt = dict()
    argv_local['LIST_TAG'] = list_tag
    return render_to_response('asset_manage/index.html', argv_local)


@login_required
@csrf_exempt
def asset_manage_show_detail(request):
    """ 资产详情 """
    asset_id = request.POST.get('asset_id', None)
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    if asset_id:
        _asset = Asset.objects.get(id=asset_id)
        _dt = dict()
        _dt['sn'] = _asset.sn
        _dt['hostname'] = _asset.name
        _dt['id'] = _asset.id
        list_property_now = _asset.property.all()
        for _lpn in list_property_now:
            try:
                _value = json.loads(_lpn.value)
            except Exception, e:
                _value = _lpn.value
            _dt[str(_lpn.property_template)] = _value
        argv_local['ASSET'] = _dt
        list_command = list()
        command = Remote_Control_Command.objects.all()
        for c in command:
            _dt = {
                "command": c.command,
                "desc": c.desc,
                "id": c.id
            }
            list_command.append(_dt)
        argv_local['LIST_COMMAND'] = list_command
        list_script = list()
        script = Remote_Control_Script.objects.all()
        for c in script:
            _dt = {
                "command": c.script,
                "desc": c.desc,
                "args": c.args,
                "id": c.id
            }
            list_script.append(_dt)
        argv_local['LIST_SCRIPT'] = list_script
        list_copy = list()
        copy = Remote_Control_Copy.objects.all()
        for c in copy:
            _dt = {
                "desc": c.desc,
                "id": c.id
            }
            list_copy.append(_dt)
        argv_local['LIST_COPY'] = list_copy
        return render_to_response('asset_manage/show_detail.html', argv_local)
    else:
        return HttpResponse(None, content_type="application/json; charset=utf-8")


@csrf_exempt
def fun_403(request):
    """
    白泽Web 权限禁止页面
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    return render_to_response('403.html', argv_local)


@csrf_exempt
def reciver(request):
    """
    白泽web接收器接入函数
    参数:
        string_name                      GET参数,接收器名称
        json信息                         POST文本,Demo: {'time': '1494230710','hostname': 'Proxy-46', 'sn': '222', 'data': [
                                                            {'time': '1494230710','hostname': 'vm-10-135-28-46', 'sn': '111', 'data': {'memory_size': '8.00 GB'}}
                                                        ]}
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
    data = request.POST.get('data', None)
    try:
        data = eval(data)
    except Exception, e:
        data = json.loads(str(data))

    for _p in data:
        try:
            string_function_name = "reciver_%s" % string_reciver_name.strip()
            json_response_data = eval(string_function_name)(_p)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"模块不存在"
            }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def network_detect(request):
    """
    白泽Web 网络探测产品
    """
    argv_local = dict()
    argv_local['USER'] = request.user.username
    return render_to_response('network_detect/network_detect.html', argv_local)


@login_required
@csrf_exempt
def network_detect_role_index(request):
    """
    白泽Web 网络探测产品 角色管理
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    _asset = Asset.objects.all()
    list_property = list()
    _dt = dict()
    for _at in _asset:
        _dt['sn'] = _at.sn
        _dt['hostname'] = _at.name
        _dt['id'] = _at.id
        # 仅仅渲染资产下拉列表不需要其他属性信息
        # list_property_now = _at.property.all()
        # for _lpn in list_property_now:
        #     try:
        #         _value = json.loads(_lpn.value)
        #     except Exception, e:
        #         _value = _lpn.value
        #     _dt[str(_lpn.property_template)] = _value
        list_property.append(_dt)
        _dt = dict()
    argv_local['LIST_PROPERTY'] = list_property

    _role = Detect_Role.objects.all()
    list_role = list()
    _lt = list()
    _dt = dict()
    for _r in _role:
        _dt['id'] = _r.id
        _dt['name'] = _r.name
        _dt['desc'] = _r.desc
        _dt['asset'] = _r.asset.name
        _dt['asset_id'] = _r.asset.id
        _dt['target'] = _r.target
        _dt['country'] = _r.geo.country
        _dt['province'] = _r.geo.province
        _dt['city'] = _r.geo.city
        _dt['area'] = _r.geo.area
        _dt['isp'] = _r.isp.name
        if _r.asset:
            _lt.append(u'探测点')
        if _r.target:
            _lt.append(u'探测目标')
        _dt['role'] = u'&'.join(_lt)
        _lt = list()
        list_role.append(_dt)
        _dt = dict()
    argv_local['LIST_ROLE'] = list_role
    argv_local['LIST_COUNTRY'] = Geo.objects.values('country').distinct()
    argv_local['LIST_PROVINCE'] = Geo.objects.values('province').distinct()
    argv_local['LIST_CITY'] = Geo.objects.values('city').distinct()
    argv_local['LIST_AREA'] = Geo.objects.values('area').distinct()
    argv_local['LIST_ISP'] = Isp.objects.values('name').distinct()
    argv_local['LIST_GEO'] = Geo.objects.values('country', 'province', 'city', 'area').distinct()

    return render_to_response('network_detect/role/index.html', argv_local)


@csrf_exempt
@login_required
@authority_url
def network_detect_role_save(request):
    """
    白泽Web 网络探测产品 新增角色
    """
    asset_id = request.POST.get('asset', '')
    role_name = request.POST.get('name', '')
    role_desc = request.POST.get('desc', '')
    target = request.POST.get('target', '')
    country = request.POST.get('country', '')
    province = request.POST.get('province', '')
    city = request.POST.get('city', '')
    area = request.POST.get('area', '')
    isp = request.POST.get('isp', '')

    if not country or not province or not city or not isp:
        response_data = {
            'success': False,
            'msg': u"添加角色失败,地域信息不完整"
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        geo = Geo.objects.get(country=country, province=province, city=city, area=area)
    except Exception,e:
        response_data = {
            'success': False,
            'msg': u"添加角色失败,地域信息不合法"
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    try:
        db_isp = Isp.objects.get(name=isp)
    except Exception,e:
        response_data = {
            'success': False,
            'msg': u"添加角色失败,运营商信息不合法"
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


    try:
        asset = Asset.objects.get(id=asset_id)
    except Exception,e:
        response_data = {
            'success': False,
            'msg': u"添加角色失败,绑定的资产不存在"
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    role = Detect_Role(name=role_name, desc=role_desc, asset=asset, target=target, geo=geo, isp=db_isp)
    try:
        role.save()
        response_data = {
            'success': True,
            'msg': u"添加角色成功"
        }
    except Exception, e:
        if str(e) == 'column name is not unique':
            response_data = {
                'success': True,
                'msg': u"该角色已经存在"
            }
        else:
            response_data = {
                'success': False,
                'msg': u"添加角色失败,error: %s" % e
            }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def network_detect_task_index(request):
    """
    白泽Web 网络探测产品 探测任务管理
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    list_task = list()
    task = Detect_Task.objects.all()
    for t in task:
        type = list()
        try:
            Ping_Detect.objects.filter(task=t)
            type.append('Ping')
        except Exception, e:
            pass
        try:
            Traceroute_Detect.objects.filter(task=t)
            type.append('Traceroute')
        except Exception, e:
            pass
        try:
            Curl_Detect.objects.filter(task=t)
            type.append('Curl')
        except Exception, e:
            pass
        type = '&'.join(type)
        _dt = {
            "id": t.id,
            "name": t.name,
            "desc": t.desc,
            "type": type,
        }
        list_task.append(_dt)
    argv_local['LIST_TASK'] = list_task
    argv_local['LIST_GEO'] = Geo.objects.values('country', 'province', 'city', 'area').distinct()
    _role = Detect_Role.objects.all()
    list_role = list()
    _lt = list()
    _dt = dict()
    for _r in _role:
        _dt['id'] = _r.id
        _dt['name'] = _r.name
        _dt['desc'] = _r.desc
        _dt['asset'] = _r.asset.name
        _dt['asset_id'] = _r.asset.id
        _dt['target'] = _r.target
        _dt['country'] = _r.geo.country
        _dt['province'] = _r.geo.province
        _dt['city'] = _r.geo.city
        _dt['area'] = _r.geo.area
        _dt['isp'] = _r.isp.name
        if _r.asset:
            _lt.append(u'探测点')
        if _r.target:
            _lt.append(u'探测目标')
        _dt['role'] = u'&'.join(_lt)
        _lt = list()
        list_role.append(_dt)
        _dt = dict()
    argv_local['LIST_ROLE'] = list_role
    return render_to_response('network_detect/task/index.html', argv_local)


def get_task(task_id, name, desc):
    """ 通过task,name,desc格式化任务"""
    data = {
        "id": task_id,
        "name": name,
        "desc": desc,
        "task_source_to_target": []
    }
    try:
        ping_detect = Ping_Detect.objects.filter(task_id=task_id)[0]
    except Exception, e:
        ping_detect = []
    if ping_detect:
        data['ping_detect_steps'] = ping_detect.steps
        data['ping_detect_num'] = ping_detect.num
        data['ping_detect_interval'] = ping_detect.interval
        data['ping_detect_timeout'] = ping_detect.timeout
        data['ping_detect_size'] = ping_detect.size
    else:
        data['ping_detect_steps'] = ''
        data['ping_detect_num'] = ''
        data['ping_detect_interval'] = ''
        data['ping_detect_timeout'] = ''
        data['ping_detect_size'] = ''


    try:
        traceroute_detect = Traceroute_Detect.objects.filter(task_id=task_id)[0]
    except Exception, e:
        traceroute_detect = []
    if traceroute_detect:
        data['traceroute_detect_steps'] = traceroute_detect.steps
        data['traceroute_detect_num'] = traceroute_detect.num
        data['traceroute_detect_timeout'] = traceroute_detect.timeout
    else:
        data['traceroute_detect_steps'] = ''
        data['traceroute_detect_num'] = ''
        data['traceroute_detect_timeout'] = ''

    try:
        curl_detect = Curl_Detect.objects.filter(task_id=task_id)[0]
    except Exception, e:
        curl_detect = []
    if curl_detect:
        data['curl_detect_steps'] = curl_detect.steps
        data['curl_detect_uri'] = curl_detect.uri
        data['curl_detect_timeout_total'] = curl_detect.timeout_total
        data['curl_detect_timeout_conn'] = curl_detect.timeout_conn
        data['curl_detect_timeout_dns'] = curl_detect.timeout_dns
    else:
        data['curl_detect_steps'] = ''
        data['curl_detect_uri'] = ''
        data['curl_detect_timeout_total'] = ''
        data['curl_detect_timeout_conn'] = ''
        data['curl_detect_timeout_dns'] = ''
    list_longitude_latitude = dict()
    ping_detect = Ping_Detect.objects.filter(task_id=task_id)
    traceroute_detect = Traceroute_Detect.objects.filter(task_id=task_id)
    curl_detect = Curl_Detect.objects.filter(task_id=task_id)
    for m in ping_detect:
        p = m.source
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        source = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        p = m.target
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        target = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        _dt = {
            "source": source,
            "target": target,
            "type": 'Ping',
            "ping_rtt": m.rtt,
            "ping_success": m.success,
            "ping_lost_rate": m.lost_rate,
            "level": 0,
            "modtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(m.modtime.timetuple()) + 8 * 60 * 60)),
        }
        if m.rtt > 100 or m.lost_rate > 5:
            _dt['level'] = 1
        if m.rtt > 200 or not m.success or m.lost_rate > 10:
            _dt['level'] = 2
        try:
            traceroute_detect_now = traceroute_detect.get(source=m.source, target=m.target)
            _dt['type'] += '&Traceroute'
            _dt['traceroute_success'] = traceroute_detect_now.success
            _dt['traceroute_data'] = traceroute_detect_now.data
        except Exception, e:
            _dt['traceroute_success'] = ''
            _dt['traceroute_data'] = ''

        try:
            curl_detect_now = curl_detect.get(source=m.source, target=m.target)
            _dt['type'] += '&Curl'
            _dt['curl_success'] = curl_detect_now.success
            _dt['curl_time_conn'] = curl_detect_now.time_conn
            _dt['curl_time_total'] = curl_detect_now.time_total
            _dt['curl_file_size'] = curl_detect_now.file_size
            _dt['curl_speed'] = curl_detect_now.speed
            level = 0
            if curl_detect_now.file_size < 1024*1024:
                if curl_detect_now.time_total > 0.5:
                    level = 1
                if curl_detect_now.time_total > 1:
                    level = 2
            else:
                if curl_detect_now.speed < 512*1024:
                    level = 1
                if curl_detect_now.speed < 216*1024:
                    level = 2
            if curl_detect_now.time_conn > 1:
                level = 1
            if curl_detect_now.time_conn > 2:
                level = 2
            if level > _dt['level']:
                _dt['level'] = level
        except Exception, e:
            _dt['curl_success'] = ''
            _dt['curl_time_conn'] = ''
            _dt['curl_time_total'] = ''
            _dt['curl_file_size'] = ''
            _dt['curl_speed'] = ''

        tag = 0
        for _dst in data['task_source_to_target']:
            if _dst['source']['name'] == _dt['source']['name'] and _dst['target']['name'] == _dt['target']['name']:
                tag = 1
        if tag == 0:
            data['task_source_to_target'].append(_dt)

    for m in traceroute_detect:
        p = m.source
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        source = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        p = m.target
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        target = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        _dt = {
            "source": source,
            "target": target,
            "ping_rtt": '',
            "ping_success": '',
            "ping_lost_rate": '',
            "type": 'Traceroute',
            "traceroute_success": m.success,
            "traceroute_data": m.data,
            "level": 0,
            "modtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(m.modtime.timetuple()) + 8 * 60 * 60)),
        }

        try:
            curl_detect_now = curl_detect.get(source=m.source, target=m.target)
            _dt['type'] += '&Curl'
            _dt['curl_success'] = curl_detect_now.success
            _dt['curl_time_conn'] = curl_detect_now.time_conn
            _dt['curl_time_total'] = curl_detect_now.time_total
            _dt['curl_file_size'] = curl_detect_now.file_size
            _dt['curl_speed'] = curl_detect_now.speed
            level = 0
            if curl_detect_now.file_size < 1024*1024:
                if curl_detect_now.time_total > 0.5:
                    level = 1
                if curl_detect_now.time_total > 1:
                    level = 2
            else:
                if curl_detect_now.speed < 512*1024:
                    level = 1
                if curl_detect_now.speed < 216*1024:
                    level = 2
            if curl_detect_now.time_conn > 1:
                level = 1
            if curl_detect_now.time_conn > 2:
                level = 2
            if level > _dt['level']:
                _dt['level'] = level
        except Exception, e:
            _dt['curl_success'] = ''
            _dt['curl_time_conn'] = ''
            _dt['curl_time_total'] = ''
            _dt['curl_file_size'] = ''
            _dt['curl_speed'] = ''

        tag = 0
        for _dst in data['task_source_to_target']:
            if _dst['source']['name'] == _dt['source']['name'] and _dst['target']['name'] == _dt['target']['name']:
                tag = 1
        if tag == 0:
            data['task_source_to_target'].append(_dt)

    for m in curl_detect:
        p = m.source
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        source = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        p = m.target
        _geo = [p.geo.country, p.geo.province, p.geo.city, p.geo.area, p.isp.name]
        for i in _geo:
            if not i:
                _geo.remove(i)
        _geo = '-'.join(_geo)
        _longitude = p.geo.longitude
        _latitude = p.geo.latitude
        while True:
            _lt = str([_longitude, _latitude])
            if _lt in list_longitude_latitude:
                if list_longitude_latitude[_lt] == p.name:
                    break
                else:
                    _longitude += 0.5
                    _latitude += 0.5
                    continue
            else:
                break
        list_longitude_latitude[str([_longitude, _latitude])] = p.name
        target = {
            "name": p.name,
            "desc": p.desc,
            "asset_id": p.asset.id,
            "country": p.geo.country,
            "province": p.geo.province,
            "city": p.geo.city,
            "area": p.geo.area,
            "isp": p.isp.name,
            "geo": _geo,
            "longitude": _longitude,
            "latitude": _latitude,
        }
        _dt = {
            "source": source,
            "target": target,
            "ping_rtt": '',
            "ping_success": '',
            "ping_lost_rate": '',
            "type": 'Curl',
            "traceroute_success": '',
            "traceroute_data": '',
            "level": 0,
            'curl_success': m.success,
            'curl_time_conn': m.time_conn,
            'curl_time_total': m.time_total,
            'curl_file_size': m.file_size,
            'curl_speed': m.speed,
            "modtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(m.modtime.timetuple()) + 8 * 60 * 60)),
        }
        if m.file_size < 1024*1024:
            if m.time_total > 0.5:
                _dt['level'] = 1
            if m.time_total > 1:
                _dt['level'] = 2
        else:
            if m.speed < 512*1024:
                _dt['level'] = 1
            if m.speed < 216*1024:
                _dt['level'] = 2
        if m.time_conn > 1:
            _dt['level'] = 1
        if m.time_conn > 2:
            _dt['level'] = 2
        tag = 0
        for _dst in data['task_source_to_target']:
            if _dst['source']['name'] == _dt['source']['name'] and _dst['target']['name'] == _dt['target']['name']:
                tag = 1
        if tag == 0:
            data['task_source_to_target'].append(_dt)
    return data


@csrf_exempt
@login_required
@authority_url
def network_detect_task_add_single(request):
    """
    白泽Web 网络探测产品 探测任务管理 添加单一任务(向任务中添加探测链路)
    return Demo:
    data = {
        "id": 0,
        "name": "test",
        "desc": "test",
        "task_source_to_target": [
            {
                'source': {'name': 'test', 'desc': 'test', 'asset_id': 0, 'country': u'中国', 'province': u'北京', 'city': u'北京', 'area': u'密云', 'geo': u'中国-北京-北京-密云', 'isp': u'电信', 'longitude': '116.4551', 'latitude': '40.2539'},
                'target': {'name': 'test', 'desc': 'test', 'asset_id': 0, 'country': u'中国', 'province': u'上海', 'city': u'上海', 'area': u'', 'geo': u'中国-上海-上海', 'isp': u'电信', 'longitude': '109.314', 'latitude': '21.6211'},
            }
        ]
    }
    """
    task_id = request.POST.get('id', '')
    task_name = request.POST.get('name', '')
    task_desc = request.POST.get('desc', '')
    ping = request.POST.get('ping', '')
    ping_detect_steps = request.POST.get('ping_detect_steps', '')
    ping_detect_num = request.POST.get('ping_detect_num', '')
    ping_detect_interval = request.POST.get('ping_detect_interval', '')
    ping_detect_timeout = request.POST.get('ping_detect_timeout', '')
    ping_detect_size = request.POST.get('ping_detect_size', '')
    traceroute = request.POST.get('traceroute', '')
    traceroute_detect_steps = request.POST.get('traceroute_detect_steps', '')
    traceroute_detect_num = request.POST.get('traceroute_detect_num', '')
    traceroute_detect_timeout = request.POST.get('traceroute_detect_timeout', '')
    curl = request.POST.get('curl', '')
    curl_detect_steps = request.POST.get('curl_detect_steps', '')
    curl_detect_timeout_dns = request.POST.get('curl_detect_timeout_dns', '')
    curl_detect_timeout_conn = request.POST.get('curl_detect_timeout_conn', '')
    curl_detect_timeout_total = request.POST.get('curl_detect_timeout_total', '')
    task_source = request.POST.get('task_source', '')
    task_target = request.POST.get('task_target', '')
    task_uri = request.POST.get('task_uri', '')
    try:
        if task_id:
            task_id = int(task_id)
        ping = json.loads(ping)
        ping_detect_steps = int(ping_detect_steps)
        ping_detect_num = int(ping_detect_num)
        ping_detect_interval = float(ping_detect_interval)
        ping_detect_timeout = int(ping_detect_timeout)
        ping_detect_size = int(ping_detect_size)
        traceroute = json.loads(traceroute)
        traceroute_detect_steps = int(traceroute_detect_steps)
        traceroute_detect_num = int(traceroute_detect_num)
        traceroute_detect_timeout = int(traceroute_detect_timeout)
        curl = json.loads(curl)
        curl_detect_steps = int(curl_detect_steps)
        curl_detect_timeout_dns = int(curl_detect_timeout_dns)
        curl_detect_timeout_conn = int(curl_detect_timeout_conn)
        curl_detect_timeout_total = int(curl_detect_timeout_total)
        task_source = int(task_source)
        task_target = int(task_target)

    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"添加探测链路失败,参数不合法",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        task_source = Detect_Role.objects.get(id=task_source)
        task_target = Detect_Role.objects.get(id=task_target)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"添加探测链路失败,探测源或者目标不存在",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        if task_id:
            task = Detect_Task.objects.get(id=task_id, name=task_name, desc=task_desc)
        else:
            task = Detect_Task.objects.get(name=task_name, desc=task_desc)
    except Exception, e:
        if task_id:
            task = Detect_Task(id=task_id, name=task_name, desc=task_desc)
        else:
            task = Detect_Task(name=task_name, desc=task_desc)
        try:
            task.save()
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"添加任务已经存在",
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    if ping:
        try:
            ping_detect = Ping_Detect.objects.get(task=task, source=task_source, target=task_target, steps=ping_detect_steps, num=ping_detect_num, interval=ping_detect_interval, timeout=ping_detect_timeout, size=ping_detect_size)
        except Exception, e:
            ping_detect = Ping_Detect(task=task, source=task_source, target=task_target, steps=ping_detect_steps, num=ping_detect_num, interval=ping_detect_interval, timeout=ping_detect_timeout, size=ping_detect_size)
            try:
                ping_detect.save()
            except Exception, e:
                response_data = {
                    'success': False,
                    'msg': u"添加任务已经存在",
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    if traceroute:
        try:
            traceroute_detect = Traceroute_Detect.objects.get(task=task, source=task_source, target=task_target, steps=traceroute_detect_steps, num=traceroute_detect_num, timeout=traceroute_detect_timeout)
        except Exception, e:
            traceroute_detect = Traceroute_Detect(task=task, source=task_source, target=task_target, steps=traceroute_detect_steps, num=traceroute_detect_num, timeout=traceroute_detect_timeout)
            try:
                traceroute_detect.save()
            except Exception, e:
                response_data = {
                    'success': False,
                    'msg': u"添加任务已经存在",
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    if curl:
        try:
            curl_detect = Curl_Detect.objects.get(task=task, source=task_source, target=task_target, steps=curl_detect_steps, timeout_total=curl_detect_timeout_total, timeout_conn=curl_detect_timeout_conn, timeout_dns=curl_detect_timeout_dns, uri=task_uri)
        except Exception, e:
            curl_detect = Curl_Detect(task=task, source=task_source, target=task_target, steps=curl_detect_steps, timeout_total=curl_detect_timeout_total, timeout_conn=curl_detect_timeout_conn, timeout_dns=curl_detect_timeout_dns, uri=task_uri)
            try:
                curl_detect.save()
            except Exception, e:
                response_data = {
                    'success': False,
                    'msg': u"添加任务已经存在",
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    task_id = task.id
    data = get_task(task_id, task.name, task.desc)
    response_data = {
        'success': True,
        'msg': u"添加任务成功",
        'data': data
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


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
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        asset = Asset.objects.get(name=hostname, sn=sn)
        detect_role = Detect_Role.objects.filter(asset=asset)
    except Exception, e:
        response_data = {
            'success': True,
            'msg': u"未找到该探测源",
            'data': []
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    list_task = []
    for role in detect_role:
        try:
            ping_detect = Ping_Detect.objects.filter(source=role)
        except Exception, e:
            ping_detect = []
        if ping_detect:
            for ping in ping_detect:
                _dt = {
                    "task_id": ping.task.id,
                    "source": ping.source.id,
                    "target": ping.target.target,
                    "target_id": ping.target.id,
                    "steps": ping.steps,
                    "num": ping.num,
                    "interval": ping.interval,
                    "timeout": ping.timeout,
                    "size": ping.size,
                    "modtime": time.mktime(ping.modtime.timetuple()) + 8 * 60 * 60,
                    "type": "ping",
                }
                list_task.append(_dt)

        try:
            traceroute_detect = Traceroute_Detect.objects.filter(source=role)
        except Exception, e:
            traceroute_detect = []
        if traceroute_detect:
            for traceroute in traceroute_detect:
                _dt = {
                    "task_id": traceroute.task.id,
                    "source": traceroute.source.id,
                    "target": traceroute.target.target,
                    "target_id": traceroute.target.id,
                    "steps": traceroute.steps,
                    "num": traceroute.num,
                    "modtime": time.mktime(traceroute.modtime.timetuple()) + 8 * 60 * 60,
                    "timeout": traceroute.timeout,
                    "type": "traceroute",
                }
                list_task.append(_dt)

        try:
            curl_detect = Curl_Detect.objects.filter(source=role)
        except Exception, e:
            curl_detect = []
        if curl_detect:
            for curl in curl_detect:
                _dt = {
                    "task_id": curl.task.id,
                    "source": curl.source.id,
                    "target": curl.target.target,
                    "target_id": curl.target.id,
                    "steps": curl.steps,
                    "uri": curl.uri,
                    "modtime": time.mktime(curl.modtime.timetuple()) + 8 * 60 * 60,
                    "timeout_total": curl.timeout_total,
                    "timeout_conn": curl.timeout_conn,
                    "timeout_dns": curl.timeout_dns,
                    "type": "curl",
                }
                list_task.append(_dt)

    response_data = {
        'success': True,
        'msg': u"成功获取探测任务",
        'data': list_task
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def network_detect_task_query_index(request):
    """任务详情"""
    task_id = request.POST.get('id', None)
    try:
        if task_id:
            task_id = int(task_id)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"查询链路信息失败,任务不存在",
            'data': str(e)
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    try:
        task = Detect_Task.objects.get(id=task_id)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"查询链路信息失败,任务不存在",
            'data': str(e)
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    data = get_task(task_id, task.name, task.desc)
    response_data = {
        'success': True,
        'msg': u"查询链路信息完成",
        'data': data
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


def do_request(url, method='POST', data={}, timeout=15):
    """ 发起http协议请求 """
    if method == 'POST':
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
        try:
            url_open = urllib2.urlopen(req, timeout=timeout)
            re = url_open.read()
            re = json.loads(re)
        except Exception, e:
            re = {
                'success': False,
                'msg': str(e)
            }
    else:
        req = urllib2.Request(url=url)
        try:
            url_open = urllib2.urlopen(req, timeout=timeout)
            re = url_open.read()
            re = json.loads(re)
        except Exception, e:
            re = {
                'success': False,
                'msg': str(e)
            }
    return re


@login_required
@csrf_exempt
def network_detect_task_query_history(request):
    """查询历史探测任务数据的API"""
    # response_data = {
    #     "success": True,
    #     "msg": u"查询历史信息成功",
    #     "data": [ [1167692400000, 61.05], [1167778800000, 58.32], [1167865200000, 57.35], [1167951600000, 56.31], [1168210800000, 55.55], [1168297200000, 55.64], [1168383600000, 54.02], [1168470000000, 51.88], [1168556400000, 52.99], [1168815600000, 52.99], [1168902000000, 51.21], [1168988400000, 52.24], [1169074800000, 50.48], [1169161200000, 51.99], [1169420400000, 51.13], [1169506800000, 55.04], [1169593200000, 55.37], [1169679600000, 54.23], [1169766000000, 55.42], [1170025200000, 54.01], [1170111600000, 56.97], [1170198000000, 58.14], [1170284400000, 58.14], [1170370800000, 59.02], [1170630000000, 58.74], [1170716400000, 58.88], [1170802800000, 57.71], [1170889200000, 59.71], [1170975600000, 59.89], [1171234800000, 57.81], [1171321200000, 59.06], [1171407600000, 58.00], [1171494000000, 57.99], [1171580400000, 59.39], [1171839600000, 59.39], [1171926000000, 58.07], [1172012400000, 60.07], [1172098800000, 61.14], [1172444400000, 61.39], [1172530800000, 61.46], [1172617200000, 61.79], [1172703600000, 62.00], [1172790000000, 60.07], [1173135600000, 60.69], [1173222000000, 61.82], [1173308400000, 60.05], [1173654000000, 58.91], [1173740400000, 57.93], [1173826800000, 58.16], [1173913200000, 57.55], [1173999600000, 57.11], [1174258800000, 56.59], [1174345200000, 59.61], [1174518000000, 61.69], [1174604400000, 62.28], [1174860000000, 62.91], [1174946400000, 62.93], [1175032800000, 64.03], [1175119200000, 66.03], [1175205600000, 65.87], [1175464800000, 64.64], [1175637600000, 64.38], [1175724000000, 64.28], [1175810400000, 64.28], [1176069600000, 61.51], [1176156000000, 61.89], [1176242400000, 62.01], [1176328800000, 63.85], [1176415200000, 63.63], [1176674400000, 63.61], [1176760800000, 63.10], [1176847200000, 63.13], [1176933600000, 61.83], [1177020000000, 63.38], [1177279200000, 64.58], [1177452000000, 65.84], [1177538400000, 65.06], [1177624800000, 66.46], [1177884000000, 64.40], [1178056800000, 63.68], [1178143200000, 63.19], [1178229600000, 61.93], [1178488800000, 61.47], [1178575200000, 61.55], [1178748000000, 61.81], [1178834400000, 62.37], [1179093600000, 62.46], [1179180000000, 63.17], [1179266400000, 62.55], [1179352800000, 64.94], [1179698400000, 66.27], [1179784800000, 65.50], [1179871200000, 65.77], [1179957600000, 64.18], [1180044000000, 65.20], [1180389600000, 63.15], [1180476000000, 63.49], [1180562400000, 65.08], [1180908000000, 66.30], [1180994400000, 65.96], [1181167200000, 66.93], [1181253600000, 65.98], [1181599200000, 65.35], [1181685600000, 66.26], [1181858400000, 68.00], [1182117600000, 69.09], [1182204000000, 69.10], [1182290400000, 68.19], [1182376800000, 68.19], [1182463200000, 69.14], [1182722400000, 68.19], [1182808800000, 67.77], [1182895200000, 68.97], [1182981600000, 69.57], [1183068000000, 70.68], [1183327200000, 71.09], [1183413600000, 70.92], [1183586400000, 71.81], [1183672800000, 72.81], [1183932000000, 72.19], [1184018400000, 72.56], [1184191200000, 72.50], [1184277600000, 74.15], [1184623200000, 75.05], [1184796000000, 75.92], [1184882400000, 75.57], [1185141600000, 74.89], [1185228000000, 73.56], [1185314400000, 75.57], [1185400800000, 74.95], [1185487200000, 76.83], [1185832800000, 78.21], [1185919200000, 76.53], [1186005600000, 76.86], [1186092000000, 76.00], [1186437600000, 71.59], [1186696800000, 71.47], [1186956000000, 71.62], [1187042400000, 71.00], [1187301600000, 71.98], [1187560800000, 71.12], [1187647200000, 69.47], [1187733600000, 69.26], [1187820000000, 69.83], [1187906400000, 71.09], [1188165600000, 71.73], [1188338400000, 73.36], [1188511200000, 74.04], [1188856800000, 76.30], [1189116000000, 77.49], [1189461600000, 78.23], [1189548000000, 79.91], [1189634400000, 80.09], [1189720800000, 79.10], [1189980000000, 80.57], [1190066400000, 81.93], [1190239200000, 83.32], [1190325600000, 81.62], [1190584800000, 80.95], [1190671200000, 79.53], [1190757600000, 80.30], [1190844000000, 82.88], [1190930400000, 81.66], [1191189600000, 80.24], [1191276000000, 80.05], [1191362400000, 79.94], [1191448800000, 81.44], [1191535200000, 81.22], [1191794400000, 79.02], [1191880800000, 80.26], [1191967200000, 80.30], [1192053600000, 83.08], [1192140000000, 83.69], [1192399200000, 86.13], [1192485600000, 87.61], [1192572000000, 87.40], [1192658400000, 89.47], [1192744800000, 88.60], [1193004000000, 87.56], [1193090400000, 87.56], [1193176800000, 87.10], [1193263200000, 91.86], [1193612400000, 93.53], [1193698800000, 94.53], [1193871600000, 95.93], [1194217200000, 93.98], [1194303600000, 96.37], [1194476400000, 95.46], [1194562800000, 96.32], [1195081200000, 93.43], [1195167600000, 95.10], [1195426800000, 94.64], [1195513200000, 95.10], [1196031600000, 97.70], [1196118000000, 94.42], [1196204400000, 90.62], [1196290800000, 91.01], [1196377200000, 88.71], [1196636400000, 88.32], [1196809200000, 90.23], [1196982000000, 88.28], [1197241200000, 87.86], [1197327600000, 90.02], [1197414000000, 92.25], [1197586800000, 90.63], [1197846000000, 90.63], [1197932400000, 90.49], [1198018800000, 91.24], [1198105200000, 91.06], [1198191600000, 90.49], [1198710000000, 96.62], [1198796400000, 96.00], [1199142000000, 99.62], [1199314800000, 99.18], [1199401200000, 95.09], [1199660400000, 96.33], [1199833200000, 95.67], [1200351600000, 91.90], [1200438000000, 90.84], [1200524400000, 90.13], [1200610800000, 90.57], [1200956400000, 89.21], [1201042800000, 86.99], [1201129200000, 89.85], [1201474800000, 90.99], [1201561200000, 91.64], [1201647600000, 92.33], [1201734000000, 91.75], [1202079600000, 90.02], [1202166000000, 88.41], [1202252400000, 87.14], [1202338800000, 88.11], [1202425200000, 91.77], [1202770800000, 92.78], [1202857200000, 93.27], [1202943600000, 95.46], [1203030000000, 95.46], [1203289200000, 101.74], [1203462000000, 98.81], [1203894000000, 100.88], [1204066800000, 99.64], [1204153200000, 102.59], [1204239600000, 101.84], [1204498800000, 99.52], [1204585200000, 99.52], [1204671600000, 104.52], [1204758000000, 105.47], [1204844400000, 105.15], [1205103600000, 108.75], [1205276400000, 109.92], [1205362800000, 110.33], [1205449200000, 110.21], [1205708400000, 105.68], [1205967600000, 101.84], [1206313200000, 100.86], [1206399600000, 101.22], [1206486000000, 105.90], [1206572400000, 107.58], [1206658800000, 105.62], [1206914400000, 101.58], [1207000800000, 100.98], [1207173600000, 103.83], [1207260000000, 106.23], [1207605600000, 108.50], [1207778400000, 110.11], [1207864800000, 110.14], [1208210400000, 113.79], [1208296800000, 114.93], [1208383200000, 114.86], [1208728800000, 117.48], [1208815200000, 118.30], [1208988000000, 116.06], [1209074400000, 118.52], [1209333600000, 118.75], [1209420000000, 113.46], [1209592800000, 112.52], [1210024800000, 121.84], [1210111200000, 123.53], [1210197600000, 123.69], [1210543200000, 124.23], [1210629600000, 125.80], [1210716000000, 126.29], [1211148000000, 127.05], [1211320800000, 129.07], [1211493600000, 132.19], [1211839200000, 128.85], [1212357600000, 127.76], [1212703200000, 138.54], [1212962400000, 136.80], [1213135200000, 136.38], [1213308000000, 134.86], [1213653600000, 134.01], [1213740000000, 136.68], [1213912800000, 135.65], [1214172000000, 134.62], [1214258400000, 134.62], [1214344800000, 134.62], [1214431200000, 139.64], [1214517600000, 140.21], [1214776800000, 140.00], [1214863200000, 140.97], [1214949600000, 143.57], [1215036000000, 145.29], [1215381600000, 141.37], [1215468000000, 136.04], [1215727200000, 146.40], [1215986400000, 145.18], [1216072800000, 138.74], [1216159200000, 134.60], [1216245600000, 129.29], [1216332000000, 130.65], [1216677600000, 127.95], [1216850400000, 127.95], [1217282400000, 122.19], [1217455200000, 124.08], [1217541600000, 125.10], [1217800800000, 121.41], [1217887200000, 119.17], [1217973600000, 118.58], [1218060000000, 120.02], [1218405600000, 114.45], [1218492000000, 113.01], [1218578400000, 116.00], [1218751200000, 113.77], [1219010400000, 112.87], [1219096800000, 114.53], [1219269600000, 114.98], [1219356000000, 114.98], [1219701600000, 116.27], [1219788000000, 118.15], [1219874400000, 115.59], [1219960800000, 115.46], [1220306400000, 109.71], [1220392800000, 109.35], [1220565600000, 106.23], [1220824800000, 106.34] ]
    # }
    source = request.POST.get('source', None)
    target = request.POST.get('target', None)
    db = request.POST.get('db', None)
    item = request.POST.get('item', None)
    period = request.POST.get('period', None)
    task_id = request.POST.get('task_id', None)
    if source:
        try:
            network_detect_source = Detect_Role.objects.get(name=source)
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"探测源不存在",
                'data': []
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            network_detect_target = Detect_Role.objects.get(name=target)
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"探测目标不存在",
                'data': []
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        request_data = {
            "source": network_detect_source.id,
            "target": network_detect_target.target,
            "db": db,
            "item": item,
            "period": period,
            "task_id": task_id
        }
        try:
            proxy_server = network_detect_source.asset.property.get(property_template_id='proxy_server')
            proxy_server = proxy_server.value.replace('"', '').strip()
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"探测源未配置Proxy Server",
                'data': []
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        url = "http://%s/proxy/network_detect/task/query/history" % proxy_server
        response_data = do_request(url, data=request_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def network_detect_task_del_single(request):
    """
    白泽Web 网络探测产品 探测任务管理 删除单一任务(向任务中添加探测链路)
    return Demo:
    data = {
        "id": 0,
        "name": "test",
        "desc": "test",
        "task_source_to_target": [
            {
                'source': {'name': 'test', 'desc': 'test', 'asset_id': 0, 'country': u'中国', 'province': u'北京', 'city': u'北京', 'area': u'密云', 'geo': u'中国-北京-北京-密云', 'isp': u'电信', 'longitude': '116.4551', 'latitude': '40.2539'},
                'target': {'name': 'test', 'desc': 'test', 'asset_id': 0, 'country': u'中国', 'province': u'上海', 'city': u'上海', 'area': u'', 'geo': u'中国-上海-上海', 'isp': u'电信', 'longitude': '109.314', 'latitude': '21.6211'},
            }
        ]
    }
    """
    task_id = request.POST.get('id', '')
    task_name = request.POST.get('name', '')
    task_desc = request.POST.get('desc', '')
    ping = request.POST.get('ping', '')
    ping_detect_steps = request.POST.get('ping_detect_steps', '')
    ping_detect_num = request.POST.get('ping_detect_num', '')
    ping_detect_interval = request.POST.get('ping_detect_interval', '')
    ping_detect_timeout = request.POST.get('ping_detect_timeout', '')
    ping_detect_size = request.POST.get('ping_detect_size', '')
    traceroute = request.POST.get('traceroute', '')
    traceroute_detect_steps = request.POST.get('traceroute_detect_steps', '')
    traceroute_detect_num = request.POST.get('traceroute_detect_num', '')
    traceroute_detect_timeout = request.POST.get('traceroute_detect_timeout', '')
    curl = request.POST.get('curl', '')
    curl_detect_steps = request.POST.get('curl_detect_steps', '')
    curl_detect_timeout_dns = request.POST.get('curl_detect_timeout_dns', '')
    curl_detect_timeout_conn = request.POST.get('curl_detect_timeout_conn', '')
    curl_detect_timeout_total = request.POST.get('curl_detect_timeout_total', '')
    task_source = request.POST.get('task_source', '')
    task_target = request.POST.get('task_target', '')
    task_uri = request.POST.get('task_uri', '')
    try:
        if task_id:
            task_id = int(task_id)
        ping = json.loads(ping)
        ping_detect_steps = int(ping_detect_steps)
        ping_detect_num = int(ping_detect_num)
        ping_detect_interval = float(ping_detect_interval)
        ping_detect_timeout = int(ping_detect_timeout)
        ping_detect_size = int(ping_detect_size)
        traceroute = json.loads(traceroute)
        traceroute_detect_steps = int(traceroute_detect_steps)
        traceroute_detect_num = int(traceroute_detect_num)
        traceroute_detect_timeout = int(traceroute_detect_timeout)
        curl = json.loads(curl)
        curl_detect_steps = int(curl_detect_steps)
        curl_detect_timeout_dns = int(curl_detect_timeout_dns)
        curl_detect_timeout_conn = int(curl_detect_timeout_conn)
        curl_detect_timeout_total = int(curl_detect_timeout_total)
        task_source = int(task_source)
        task_target = int(task_target)

    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"删除探测链路失败,参数不合法",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        task_source = Detect_Role.objects.get(id=task_source)
        task_target = Detect_Role.objects.get(id=task_target)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"删除探测链路失败,探测源或者目标不存在",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    try:
        if task_id:
            task = Detect_Task.objects.get(id=task_id, name=task_name, desc=task_desc)
        else:
            task = Detect_Task.objects.get(name=task_name, desc=task_desc)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"删除探测链路失败,任务不存在",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    if ping:
        try:
            ping_detect = Ping_Detect.objects.get(task=task, source=task_source, target=task_target)
            ping_detect.delete()
        except Exception, e:
            pass
    if traceroute:
        try:
            traceroute_detect = Traceroute_Detect.objects.get(task=task, source=task_source, target=task_target)
            traceroute_detect.delete()
        except Exception, e:
            pass

    if curl:
        try:
            curl_detect = Curl_Detect.objects.get(task=task, source=task_source, target=task_target, uri=task_uri)
            curl_detect.delete()
        except Exception, e:
            pass
    task_id = task.id
    data = get_task(task_id, task.name, task.desc)
    response_data = {
        'success': True,
        'msg': u"删除任务成功",
        'data': data
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def network_detect_role_delete_multiple(request):
    """ 批量删除探测角色 """
    list_role = request.POST.get('role', '')
    try:
        list_role = eval(list_role)
    except Exception, e:
        list_role = json.loads(str(list_role))
    try:
        for role_id in list_role:
            Detect_Role.objects.get(id=role_id).delete()
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"删除角色失败",
            'data': e
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    response_data = {
        'success': True,
        'msg': u"删除角色成功",
        'data': list_role
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def network_detect_task_delete_multiple(request):
    """ 批量删除探测任务 """
    list_task = request.POST.get('task', '')
    try:
        list_task = eval(list_task)
    except Exception, e:
        list_task = json.loads(str(list_task))
    try:
        for task_id in list_task:
            Detect_Task.objects.get(id=task_id).delete()
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"删除任务失败",
            'data': e
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    response_data = {
        'success': True,
        'msg': u"删除任务成功",
        'data': list_task
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def remote_control_add_command(request):
    desc = request.POST.get('desc', '')
    command = request.POST.get('command', '')
    if desc and command:
        try:
            db_command = Remote_Control_Command.objects.get(desc=desc, command=command)
        except Exception, e:
            db_command = Remote_Control_Command(desc=desc, command=command)
            db_command.save()
        response_data = {
            'success': True,
            'msg': u"添加命令成功",
            'data': {
                'command_id': db_command.id,
                'desc': db_command.desc
            }
        }
    else:
        response_data = {
            'success': False,
            'msg': u"添加命令失败",
            'data': {'command_id': -1, 'desc': ''}
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def remote_control_del_command(request):
    command_id = request.POST.get('command_id', '')
    if command_id:
        try:
            db_command = Remote_Control_Command.objects.get(id=command_id)
            desc = db_command.desc
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"命令不存在",
                'data': {'command_id': -1, 'desc': ''}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        db_command.delete()
        response_data = {
            'success': True,
            'msg': u"删除命令成功",
            'data': {
                'command_id': command_id,
                'desc': desc
            }
        }
    else:
        response_data = {
            'success': False,
            'msg': u"删除命令失败",
            'data': {'command_id': -1, 'desc': ''}
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def remote_control_do_command(request):
    command_id = request.POST.get('command_id', '')
    agent_id = request.POST.get('agent_id', '')
    agent_tag_id = request.POST.get('agent_tag', '')
    if agent_tag_id:
        try:
            _asset_tag = Asset_Tag.objects.get(id=agent_tag_id)
            agent_id = _asset_tag.asset.all()[0].id
        except Exception, e:
            pass
    if command_id and agent_id:
        try:
            db_command = Remote_Control_Command.objects.get(id=command_id)
            desc = db_command.desc
            command = db_command.command
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"命令不存在",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            asset = Asset.objects.get(id=agent_id)
            sn = asset.sn
            proxy_server = asset.property.get(property_template_id='proxy_server')
            proxy_server = proxy_server.value.replace('"', '').strip()
            remote_control_server = asset.property.get(property_template_id='remote_control_server')
            remote_control_server = remote_control_server.value.replace('"', '').strip()
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"执行命令失败,该资产未配置Proxy Server",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        url = "http://%s/proxy/remote_control/" % proxy_server
        str_module_args = {"command": command}
        json_post_data = {"string_module_name": "shell", "string_module_args": str_module_args, "string_agents": [remote_control_server], "sn": sn}
        json_post_data = json.loads(json.dumps(json_post_data))
        data = do_request(url, data=json_post_data)
        if data['success']:
            response_data = {
                'success': True,
                'msg': u"执行命令成功",
                'data': data['data'][0]
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        else:
            if 'data' in data:
                _dt = data['data']
            else:
                _dt = ''
            response_data = {
                'success': False,
                'msg': u"执行命令失败,请检查网络通信",
                'data': _dt
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"执行命令失败,传递的参数异常",
            'data': None
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def remote_control_add_script(request):
    desc = request.POST.get('desc', '')
    args = request.POST.get('args', '')
    script = request.FILES.get('script', '')
    fp_file_data = script.read()
    try:
        args = json.loads(args)
    except Exception, e:
        response_data = {
            'success': False,
            'msg': u"添加脚本失败",
            'data': {'command_id': -1, 'desc': ''}
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    if desc and script:
        try:
            db_script = Remote_Control_Script.objects.get(desc=desc)
            response_data = {
                'success': True,
                'msg': u"该描述的脚本已经存在",
                'data': {'script_id': db_script.id, 'desc': db_script.desc, 'script_args': db_script.args}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        except Exception, e:
            file_name = "Script_%.6f" % time.time()
            file_full_path = os.path.join(C.UPLOAD_ROOT, file_name)
            if not os.path.exists(C.UPLOAD_ROOT):
                os.makedirs(C.UPLOAD_ROOT)
            try:
                fp = open(file_full_path, 'wb+')
                fp.write(fp_file_data)
                fp.close()
            except Exception, e:
                errInfo = u'上传脚本写入失败,Exception: %s' % str(e)
                response_data = {
                    'success': False,
                    'msg': errInfo,
                    'data': {'command_id': -1, 'desc': ''}
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
            db_script = Remote_Control_Script(desc=desc, script=file_full_path, args=args)
            db_script.save()
            response_data = {
                'success': True,
                'msg': u"添加脚本成功",
                'data': {'script_id': db_script.id, 'desc': db_script.desc, 'script_args': db_script.args}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"添加脚本失败",
            'data': {'script_id': -1, 'desc': ''}
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def remote_control_del_script(request):
    script_id = request.POST.get('script_id', '')
    if script_id:
        try:
            db_script = Remote_Control_Script.objects.get(id=script_id)
            desc = db_script.desc
            script = db_script.script
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"脚本不存在",
                'data': {'script_id': -1, 'desc': ''}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            os.remove(script)
        except Exception, e:
            pass
        db_script.delete()
        response_data = {
            'success': True,
            'msg': u"删除脚本成功",
            'data': {
                'script_id': script_id,
                'desc': desc
            }
        }
    else:
        response_data = {
            'success': False,
            'msg': u"删除脚本失败",
            'data': {'script_id': -1, 'desc': ''}
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def remote_control_do_script(request):
    script_id = request.POST.get('script_id', '')
    agent_id = request.POST.get('agent_id', '')
    script_args = request.POST.get('script_args', '')
    agent_tag_id = request.POST.get('agent_tag', '')
    if agent_tag_id:
        try:
            _asset_tag = Asset_Tag.objects.get(id=agent_tag_id)
            agent_id = _asset_tag.asset.all()[0].id
        except Exception, e:
            pass
    if script_id and agent_id:
        try:
            db_script = Remote_Control_Script.objects.get(id=script_id)
            desc = db_script.desc
            script = db_script.script
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"脚本不存在",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            asset = Asset.objects.get(id=agent_id)
            sn = asset.sn
            proxy_server = asset.property.get(property_template_id='proxy_server')
            proxy_server = proxy_server.value.replace('"', '').strip()
            remote_control_server = asset.property.get(property_template_id='remote_control_server')
            remote_control_server = remote_control_server.value.replace('"', '').strip()
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"执行脚本失败,该资产未配置Proxy Server",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        url = "http://%s/proxy/remote_control/" % proxy_server
        list_file_data = open(script, 'r').readlines()
        str_module_args = {"script": list_file_data, "args": script_args}
        json_post_data = {"string_module_name": "script", "string_module_args": str_module_args, "string_agents": [remote_control_server], "sn": sn}
        json_post_data = json.loads(json.dumps(json_post_data))
        data = do_request(url, data=json_post_data)
        if data['success']:
            response_data = {
                'success': True,
                'msg': u"执行脚本成功",
                'data': data['data'][0]
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        else:
            response_data = {
                'success': False,
                'msg': u"执行脚本失败",
                'data': data['data']
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"执行脚本失败",
            'data': None
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


def download_file(copy_src, file_full_path, with_pass, username, password):
    url = urlparse(copy_src)
    if url.scheme.lower() == 'ftp':
        port = url.port if url.port else 21
        ftp = FTP()
        ftp.set_debuglevel(2)
        try:
            ftp.connect(url.hostname, port, timeout=10)
            if with_pass:
                ftp.login(username, password)
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"无法连接复制动作原地址",
                'data': {'copy_id': -1, 'desc': ''}
            }
            return response_data
        path = url.path
        ftp_filepath, ftp_filename = os.path.split(path)
        bufsize = 4096
        codes = ['UTF-8', 'gbk', 'GB2312', 'GB18030', 'Big5', 'HZ']
        for c in codes:
            try:
                ftp.cwd(ftp_filepath.encode(c))
                msg = "RETR %s".encode(c) % ftp_filename
                ftp_filename = ftp_filename.encode(c)
                break
            except Exception, e:
                continue
        try:
            fp = open(file_full_path, 'wb+')
            ftp.retrbinary(msg, fp.write, bufsize)
            ftp_filesize = ftp.size(ftp_filename)
            fp.close()
            ftp.set_debuglevel(0)
            ftp.quit()
        except Exception, e:
            errInfo = u'ftp下载失败,请检查下载地址'
            response_data = {
                'success': False,
                'msg': errInfo,
                'data': {'command_id': -1, 'desc': ''}
            }
            return response_data
        if os.path.getsize(file_full_path) != ftp_filesize:
            errInfo = u'ftp下载失败,下载文件大小不一致'
            response_data = {
                'success': False,
                'msg': errInfo,
                'data': {'command_id': -1, 'desc': ''}
            }
            return response_data
    elif url.scheme.lower() == 'http':
        try:
            urllib.urlretrieve(copy_src, file_full_path)
        except Exception, e:
            errInfo = u'http下载失败,请检查下载地址'
            response_data = {
                'success': False,
                'msg': errInfo,
                'data': {'command_id': -1, 'desc': ''}
            }
            return response_data
    else:
        response_data = {
            'success': False,
            'msg': u"复制动作原地址协议不支持",
            'data': {'copy_id': -1, 'desc': ''}
        }
        return response_data
    response_data = {
        'success': True,
        'msg': u"下载成功",
        'data': {}
    }
    return response_data


@csrf_exempt
@login_required
@authority_url
def remote_control_add_copy(request):
    desc = request.POST.get('desc', '')
    copy_dest = request.POST.get('copy_dest', '')
    authority = request.POST.get('authority', '755')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    try:
        copy_src = request.FILES.get('copy_src', '')
        fp_file_data = copy_src.read()
        copy_src_type = 'file'
    except Exception, e:
        copy_src = request.POST.get('copy_src', '')
        copy_src_type = 'text'

    file_name = "Copy_%.6f" % time.time()
    file_full_path = os.path.join(C.UPLOAD_ROOT, file_name)
    if not os.path.exists(C.UPLOAD_ROOT):
        os.makedirs(C.UPLOAD_ROOT)

    if desc and copy_src:
        if copy_src_type == 'file':
            copy_src = ''
            try:
                fp = open(file_full_path, 'wb+')
                fp.write(fp_file_data)
                fp.close()
            except Exception, e:
                errInfo = u'上传文件写入失败,Exception: %s' % str(e)
                response_data = {
                    'success': False,
                    'msg': errInfo,
                    'data': {'command_id': -1, 'desc': ''}
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            db_copy = Remote_Control_Copy.objects.get(desc=desc)
            try:
                os.remove(db_copy.src)
            except Exception, e:
                pass
            db_copy.src = file_full_path
            db_copy.dest = copy_dest
            db_copy.authority = authority
            db_copy.src_url = copy_src
            db_copy.src_username = username
            db_copy.src_password = password
        except Exception, e:
            db_copy = Remote_Control_Copy(desc=desc, src=file_full_path, dest=copy_dest, authority=authority, src_url=copy_src, src_username=username, src_password=password)
        db_copy.save()
        response_data = {
            'success': True,
            'msg': u"添加动作成功",
            'data': {'copy_id': db_copy.id, 'desc': db_copy.desc}
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"添加动作失败",
            'data': {'copy_id': -1, 'desc': ''}
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def remote_control_del_copy(request):
    copy_id = request.POST.get('copy_id', '')
    if copy_id:
        try:
            db_copy = Remote_Control_Copy.objects.get(id=copy_id)
            desc = db_copy.desc
            src = db_copy.src
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"文件不存在",
                'data': {'copy_id': -1, 'desc': ''}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            os.remove(src)
        except Exception, e:
            pass
        db_copy.delete()
        response_data = {
            'success': True,
            'msg': u"删除动作成功",
            'data': {
                'copy_id': copy_id,
                'desc': desc
            }
        }
    else:
        response_data = {
            'success': False,
            'msg': u"删除动作失败",
            'data': {'copy_id': -1, 'desc': ''}
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def remote_control_do_copy(request):
    copy_id = request.POST.get('copy_id', '')
    agent_id = request.POST.get('agent_id', '')
    agent_tag_id = request.POST.get('agent_tag', '')
    if agent_tag_id:
        try:
            _asset_tag = Asset_Tag.objects.get(id=agent_tag_id)
            agent_id = _asset_tag.asset.all()[0].id
        except Exception, e:
            pass
    if copy_id and agent_id:
        try:
            db_copy = Remote_Control_Copy.objects.get(id=copy_id)
            src = db_copy.src
            dest = db_copy.dest
            authority = db_copy.authority
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"动作不存在",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        try:
            asset = Asset.objects.get(id=agent_id)
            sn = asset.sn
            proxy_server = asset.property.get(property_template_id='proxy_server')
            proxy_server = proxy_server.value.replace('"', '').strip()
            remote_control_server = asset.property.get(property_template_id='remote_control_server')
            remote_control_server = remote_control_server.value.replace('"', '').strip()
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"执行动作失败,该资产未配置Proxy Server",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        url = "http://%s/proxy/remote_control/" % proxy_server
        list_file_data = open(src, 'r').readlines()
        str_module_args = {"src": list_file_data, "dest": dest, "mode": authority}
        json_post_data = {"string_module_name": "copy", "string_module_args": str_module_args, "string_agents": [remote_control_server], "sn": sn}
        json_post_data = json.loads(json.dumps(json_post_data))
        data = do_request(url, data=json_post_data)
        if data['success']:
            response_data = {
                'success': True,
                'msg': u"执行动作成功",
                'data': data['data'][0]
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        else:
            response_data = {
                'success': False,
                'msg': u"执行动作失败",
                'data': data['data']
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"执行动作失败",
            'data': None
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def asset_manage_tag_add(request):
    """ 添加Tag """
    tag_name = request.POST.get('tag_name', '')
    if tag_name:
        try:
            Asset_Tag.objects.get(name=tag_name)
            response_data = {
                'success': True,
                'msg': u"添加Tag已存在",
                'data': None
            }
        except Exception, e:
            asset_tag = Asset_Tag(name=tag_name, ontree=False)
            asset_tag.save()
            response_data = {
                'success': True,
                'msg': u"添加Tag成功",
                'data': None
            }
    else:
        response_data = {
            'success': False,
            'msg': u"添加Tag失败",
            'data': None
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def asset_manage_tag_query(request):
    """ 查询Tag """
    tag_pattern = request.POST.get('tag_pattern', '')
    if tag_pattern:
        try:
            list_tag = list()
            _dt = dict()
            _asset_tag = Asset_Tag.objects.filter(name__icontains=tag_pattern)
            for _at in _asset_tag:
                _dt['name'] = _at.name
                _dt['id'] = _at.id
                list_tag.append(_dt)
                _dt = dict()
            response_data = {
                'success': True,
                'msg': u"搜索成功",
                'data': list_tag
            }
        except Exception, e:
            response_data = {
                'success': True,
                'msg': u"搜索结果为空",
                'data': []
            }
    else:
        response_data = {
            'success': False,
            'msg': u"搜索失败",
            'data': None
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def asset_manage_tag_unbind(request):
    tag_name = request.POST.get('tag_name', '')
    asset_id = request.POST.get('asset_id', '')
    if tag_name and asset_id:
        try:
            asset_tag = Asset_Tag.objects.get(name=tag_name)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"Tag不存在",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        try:
            Asset_Tag_Data.objects.get(asset_id=int(asset_id), asset_tag=asset_tag).delete()
            json_response_data = {
                "success": True,
                "msg": u"取消绑定成功",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"取消绑定失败",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    else:
        json_response_data = {
            "success": False,
            "msg": u"参数异常",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

@csrf_exempt
@login_required
@authority_url
def asset_manage_tag_bind(request):
    """ 对Tag绑定资产 """
    tag_id = request.POST.get('tag_id', '')
    string_asset_id = request.POST.get('asset', '')
    if tag_id:
        try:
            list_asset_id = eval(string_asset_id)
        except Exception, e:
            try:
                list_asset_id = json.loads(str(string_asset_id))
            except Exception, e:
                json_response_data = {
                    "success": False,
                    "msg": u"资产列表不合法",
                    'data': None
                }
                return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        try:
            _asset_tag = Asset_Tag.objects.get(id=tag_id)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"Tag不存在",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

        for _asset_id in list_asset_id:
            try:
                Asset_Tag_Data.objects.get(asset_tag=_asset_tag, asset_id=_asset_id)
            except Exception, e:
                _asset_tag_data = Asset_Tag_Data(asset_tag=_asset_tag, asset_id=_asset_id)
                _asset_tag_data.save()

        json_response_data = {
            "success": True,
            "msg": u"绑定资产成功",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    else:
        json_response_data = {
            "success": False,
            "msg": u"Tag不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def asset_manage_tag_query_asset(request):
    """ 查询Tag绑定的资产 """
    tag_id = request.POST.get('tag_id', '')
    tag_name = request.POST.get('tag_name', '')
    if tag_name == u'空闲资源池':
        try:
            list_asset_id_on_tree = list()
            list_asset_id_off_tree = list()
            _dt = dict()
            _asset_tag = Asset_Tag.objects.filter(ontree=True)
            for _at in _asset_tag:
                _asset = _at.asset.all()
                for _a in _asset:
                    if _a.id not in list_asset_id_on_tree:
                        list_asset_id_on_tree.append(_a.id)
            _asset = Asset.objects.all()
            for _at in _asset:
                if _at.id not in list_asset_id_on_tree:
                    _dt['sn'] = _at.sn
                    _dt['hostname'] = _at.name
                    _dt['id'] = _at.id
                    list_tag_name = []
                    try:
                        asset_tag_data = Asset_Tag_Data.objects.filter(asset=_at)
                        for atd in asset_tag_data:
                            if not atd.asset_tag.ontree:
                                list_tag_name.append(atd.asset_tag.name)
                    except Exception, e:
                        pass
                    _dt['tag_list'] = list_tag_name
                    list_property_now = _at.property.all()
                    for _lpn in list_property_now:
                        try:
                            _value = json.loads(_lpn.value)
                        except Exception, e:
                            _value = _lpn.value
                        _dt[str(_lpn.property_template)] = _value
                    list_asset_id_off_tree.append(_dt)
                _dt = dict()
            json_response_data = {
                "success": True,
                "msg": u"查询Tag资产完成",
                'data': list_asset_id_off_tree[:100]
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"无空闲资产",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    if tag_id:
        try:
            _asset_tag = Asset_Tag.objects.get(id=tag_id)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"Tag不存在",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

        _asset = _asset_tag.asset.all()
        list_property = list()
        _dt = dict()
        for _at in _asset:
            _dt['sn'] = _at.sn
            _dt['hostname'] = _at.name
            _dt['id'] = _at.id
            list_tag_name = []
            try:
                asset_tag_data = Asset_Tag_Data.objects.filter(asset=_at)
                for atd in asset_tag_data:
                    if not atd.asset_tag.ontree:
                        list_tag_name.append(atd.asset_tag.name)
            except Exception, e:
                pass
            _dt['tag_list'] = list_tag_name
            list_property_now = _at.property.all()
            for _lpn in list_property_now:
                try:
                    _value = json.loads(_lpn.value)
                except Exception, e:
                    _value = _lpn.value
                _dt[str(_lpn.property_template)] = _value
            list_property.append(_dt)
            _dt = dict()
        json_response_data = {
            "success": True,
            "msg": u"查询Tag资产完成",
            'data': list_property
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    elif tag_name:
        try:
            _asset_tag = Asset_Tag.objects.get(name=tag_name)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"Tag不存在",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

        _asset = _asset_tag.asset.all()
        list_property = list()
        _dt = dict()
        for _at in _asset:
            _dt['sn'] = _at.sn
            _dt['hostname'] = _at.name
            _dt['id'] = _at.id
            list_tag_name = []
            try:
                asset_tag_data = Asset_Tag_Data.objects.filter(asset=_at)
                for atd in asset_tag_data:
                    if not atd.asset_tag.ontree:
                        list_tag_name.append(atd.asset_tag.name)
            except Exception, e:
                pass
            _dt['tag_list'] = list_tag_name
            list_property_now = _at.property.all()
            for _lpn in list_property_now:
                try:
                    _value = json.loads(_lpn.value)
                except Exception, e:
                    _value = _lpn.value
                _dt[str(_lpn.property_template)] = _value
            list_property.append(_dt)
            _dt = dict()
        json_response_data = {
            "success": True,
            "msg": u"查询Tag资产完成",
            'data': list_property
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    else:
        json_response_data = {
            "success": False,
            "msg": u"Tag非法",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def asset_manage_tag_del(request):
    """ 删除Tag """
    tag_name = request.POST.get('tag_name', '')
    if tag_name:
        try:
            _asset_tag = Asset_Tag.objects.get(name=tag_name)
            _asset_tag.delete()
            response_data = {
                'success': True,
                'msg': u"删除Tag成功",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"Tag不存在",
                'data': None
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    else:
        response_data = {
            'success': False,
            'msg': u"Tag名称不合法",
            'data': None
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def asset_manage_tree_save(request):
    """ 保存资产目录树 """
    string_json_tree = request.POST.get('json_tree', '').encode('utf-8')
    try:
        json_tree = eval(string_json_tree)
    except Exception, e:
        try:
            json_tree = json.loads(str(string_json_tree))
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"资产树不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    tree_name = json_tree[0]['text']
    try:
        bussiness_tree = Business_Tree.objects.get(name=tree_name)
        bussiness_tree.data = json_tree
    except Exception, e:
        bussiness_tree  = Business_Tree(name=tree_name, data=json_tree)
    try:
        bussiness_tree.save()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"资产树保存失败",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    json_response_data = {
        "success": True,
        "msg": u"资产树保存成功",
        'data': json_tree
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def asset_manage_tree_query(request):
    """ 查询资产目录树 """
    tree_name = request.POST.get('name', '').encode('utf-8')
    try:
        bussiness_tree = Business_Tree.objects.get(name=tree_name)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"资产树尚未注册,请添加资产树,根节点名称为:已分配资源池",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    try:
        json_tree = eval(bussiness_tree.data)
    except Exception, e:
        try:
            json_tree = json.loads(str(bussiness_tree.data))
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"资产树不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    json_response_data = {
        "success": True,
        "msg": u"资产树查询成功",
        'data': json_tree
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def asset_manage_tree_bind(request):
    """ 绑定资产目录树 """
    tag_name = request.POST.get('node', '')
    string_asset_id = request.POST.get('asset', '')
    if tag_name:
        try:
            list_asset_id = eval(string_asset_id)
        except Exception, e:
            try:
                list_asset_id = json.loads(str(string_asset_id))
            except Exception, e:
                json_response_data = {
                    "success": False,
                    "msg": u"绑定目录树的资产列表不合法",
                    'data': None
                }
                return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        try:
            _asset_tag = Asset_Tag.objects.get(name=tag_name)
        except Exception, e:
            _asset_tag = Asset_Tag(name=tag_name)
            _asset_tag.save()

        for _asset_id in list_asset_id:
            try:
                Asset_Tag_Data.objects.get(asset_tag=_asset_tag, asset_id=_asset_id)
            except Exception, e:
                _asset_tag_data = Asset_Tag_Data(asset_tag=_asset_tag, asset_id=_asset_id)
                _asset_tag_data.save()

        json_response_data = {
            "success": True,
            "msg": u"绑定目录树成功",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    else:
        json_response_data = {
            "success": False,
            "msg": u"绑定目录树的tag不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def configure_manage(request):
    """配置管理页
    参数：
        无
    返回值：
        配置管理页面的html代码
    页面渲染变量：
        无
    """
    argv_local = dict()
    argv_local['USER'] = request.user.username
    return render_to_response('configure_manage/configure_manage.html', argv_local)


@login_required
@csrf_exempt
def work_manage(request):
    """作业管理页
    参数：
        无
    返回值：
        作业管理内嵌页的html代码
    页面渲染变量：
        BODY_BG                                     页面背景色,默认值白色(white-bg)
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    _work = Configure_Manage_Work.objects.all()
    list_work = list()
    for w in _work:
        _dt = {
            "id": w.id,
            "name_en": w.name_en,
            "name_cn": w.name_cn,
            "status": w.status,
        }
        list_work.append(_dt)
    argv_local['LIST_WORK'] = list_work
    return render_to_response('work_manage/work_manage.html', argv_local)


@login_required
@csrf_exempt
def task_manage(request):
    """任务管理页
    参数：
        无
    返回值：
        任务管理内嵌页的html代码
    页面渲染变量：
        BODY_BG                                     页面背景色,默认值白色(white-bg)
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    _task = Configure_Manage_Task.objects.all()
    list_task = list()
    for t in _task:
        _dt = {
            "id": t.id,
            "name_en": t.name_en,
            "name_cn": t.name_cn,
            "status": t.status,
        }
        list_task.append(_dt)
    argv_local['LIST_TASK'] = list_task
    return render_to_response('task_manage/task_manage.html', argv_local)


@csrf_exempt
@login_required
@authority_url
def task_manage_add(request):
    """新增任务页
    参数：
        无
    返回值：
        新增任务内嵌页的html代码
    页面渲染变量：
        BODY_BG                                     页面背景色,默认值白色(white-bg)
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    _work = Configure_Manage_Work.objects.all()
    list_work = list()
    for w in _work:
        _dt = {
            "id": w.id,
            "name_en": w.name_en,
            "name_cn": w.name_cn,
            "status": w.status,
        }
        list_work.append(_dt)
    argv_local['LIST_WORK'] = list_work
    return render_to_response('task_manage/add.html', argv_local)


@csrf_exempt
@login_required
@authority_url
def work_manage_add(request):
    """新增作业页
    参数：
        无
    返回值：
        新增作业内嵌页的html代码
    页面渲染变量：
        BODY_BG                                     页面背景色,默认值白色(white-bg)
    """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    list_command = list()
    command = Remote_Control_Command.objects.all()
    for c in command:
        _dt = {
            "command": c.command,
            "desc": c.desc,
            "id": c.id
        }
        list_command.append(_dt)
    argv_local['LIST_COMMAND'] = list_command
    list_script = list()
    script = Remote_Control_Script.objects.all()
    for c in script:
        _dt = {
            "command": c.script,
            "desc": c.desc,
            "args": c.args,
            "id": c.id
        }
        list_script.append(_dt)
    argv_local['LIST_SCRIPT'] = list_script
    list_copy = list()
    copy = Remote_Control_Copy.objects.all()
    for c in copy:
        _dt = {
            "desc": c.desc,
            "id": c.id
        }
        list_copy.append(_dt)
    argv_local['LIST_COPY'] = list_copy
    list_tag = list()
    _asset_tag = Asset_Tag.objects.filter(ontree=False)
    _dt = dict()
    for _at in _asset_tag:
        _dt['id'] = _at.id
        _dt['name'] = _at.name
        list_tag.append(_dt)
        _dt = dict()
    argv_local['LIST_TAG'] = list_tag
    return render_to_response('work_manage/add.html', argv_local)


def delete_all_result(id):
    """ 基于作业id删除该作业的结果"""
    _work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work_id=id)
    for wrd in _work_result_data:
        wrd.result.delete()


def check_task_status_from_work(work):
    if work.status == 1 or work.status == 4:
        return False
    configure_manage_task_data = work.Configure_Manage_Task_Data.all()
    for cmtd in configure_manage_task_data:
        t = cmtd.task
        if t.status == 1 or t.status == 4:
            return False
    return True


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_save(request):
    """ 配置管理添加作业"""
    name_cn = request.POST.get('name_cn', '')
    name_en = request.POST.get('name_en', '')
    timeout = request.POST.get('timeout', '')
    sync = request.POST.get('sync', '')
    desc = request.POST.get('desc', '')
    test_tag_id = request.POST.get('test_tag', '')
    string_jobs = request.POST.get('jobs', '').encode('utf-8')
    string_tags = request.POST.get('tags', '').encode('utf-8')
    try:
        json_tags = eval(string_tags)
    except Exception, e:
        try:
            json_tags = json.loads(str(string_tags))
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"参数不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(name_en=name_en)
        if not check_task_status_from_work(_configure_manage_work):
            json_response_data = {
                "success": False,
                "msg": u"作业锁定中",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        _configure_manage_work.name_cn = name_cn
        _configure_manage_work.timeout = timeout
        _configure_manage_work.sync = sync
        _configure_manage_work.desc = desc
        _configure_manage_work.test_tag_id = test_tag_id
        _configure_manage_work.jobs = string_jobs
        _configure_manage_work.status = 0
        _configure_manage_work.save()
        delete_all_result(_configure_manage_work.id)
        try:
            Configure_Manage_Work_Tag_Data.objects.filter(work=_configure_manage_work).delete()
        except Exception, e:
            pass
    except Exception, e:
        _configure_manage_work = Configure_Manage_Work(name_en=name_en, name_cn=name_cn, timeout=timeout, sync=sync, desc=desc, test_tag_id=test_tag_id, jobs=string_jobs)
        _configure_manage_work.save()
    for tag in json_tags:
        _work_tag_data = Configure_Manage_Work_Tag_Data(work=_configure_manage_work, asset_tag_id=tag)
        _work_tag_data.save()
    data = {
        "id": _configure_manage_work.id
    }
    json_response_data = {
        "success": True,
        "msg": u"保存作业成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_test(request):
    """ 配置管理作业测试"""
    id = request.POST.get('id', '')
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
        if not check_task_status_from_work(_configure_manage_work):
            json_response_data = {
                "success": False,
                "msg": u"作业锁定中",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        jobs = _configure_manage_work.jobs
        if not isinstance(jobs, list):
            jobs = json.loads(jobs)
        for j in jobs:
            if not isinstance(j, dict):
                j = json.loads(j)
            if j['type'] == 'copy':
                remote_control_copy = Remote_Control_Copy.objects.get(id=int(j['id']))
                if remote_control_copy.src_url:
                    if remote_control_copy.src_username or remote_control_copy.src_password:
                        with_pass = True
                    else:
                        with_pass = False
                    re = download_file(remote_control_copy.src_url, remote_control_copy.src, with_pass, remote_control_copy.src_username, remote_control_copy.src_password)
                    if not re['success'] and not j['ignore_error']:
                        return HttpResponse(json.dumps(re), content_type="application/json; charset=utf-8")
        _configure_manage_work.status = 1
        _configure_manage_work.save()
        try:
            _configure_manage_work.result.all().delete()
        except Exception, e:
            pass
    except Exception,e:
        json_response_data = {
            "success": False,
            "msg": u"作业不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"测试作业开始",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


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
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
    list_tag_id = []
    try:
        asset = Asset.objects.get(name=hostname, sn=sn)
        asset_tag_data = Asset_Tag_Data.objects.filter(asset=asset)
        for atd in asset_tag_data:
            if not atd.asset_tag.ontree:
                list_tag_id.append(atd.asset_tag.id)
    except Exception, e:
        response_data = {
            'success': True,
            'msg': u"该资产未绑定tag",
            'data': []
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")

    list_work = []
    try:
        _work = Configure_Manage_Work.objects.filter(status=1).filter(test_tag_id__in=list_tag_id)
        for _w in _work:
            try:
                Configure_Manage_Work_Result_Data.objects.get(work=_w, asset=asset)
            except Exception, e:
                list_jobs = []
                jobs = _w.jobs
                if not isinstance(jobs, list):
                    jobs = json.loads(jobs)
                for j in jobs:
                    if not isinstance(j, dict):
                        j = json.loads(j)
                    if j['type'] == 'command':
                        job_now = Remote_Control_Command.objects.get(id=j['id'])
                        _dtt = {
                            "id": job_now.id,
                            "ignore_error": j['ignore_error'],
                            "desc": job_now.desc,
                            "command": job_now.command,
                            "type": "command",
                        }
                    elif j['type'] == 'script':
                        job_now = Remote_Control_Script.objects.get(id=j['id'])
                        _dtt = {
                            "id": job_now.id,
                            "ignore_error": j['ignore_error'],
                            "desc": job_now.desc,
                            "args": j['args'],
                            "script": open(job_now.script, 'r').readlines(),
                            "type": "script",
                            "md5": hashlib.md5(open(job_now.script, 'rb').read()).hexdigest(),
                        }
                    elif j['type'] == 'copy':
                        job_now = Remote_Control_Copy.objects.get(id=j['id'])
                        _dtt = {
                            "id": job_now.id,
                            "ignore_error": j['ignore_error'],
                            "desc": job_now.desc,
                            "dest": j['dest'],
                            "authority": j['authority'],
                            "src": base64.b64encode(open(job_now.src, 'rb').read()),
                            "type": "copy",
                            "check_change": j['check_change'],
                            "md5": hashlib.md5(open(job_now.src, 'rb').read()).hexdigest(),
                        }
                    list_jobs.append(_dtt)
                _dt = {
                    "id": _w.id,
                    "name_cn": _w.name_cn,
                    "name_en": _w.name_en,
                    "desc": _w.desc,
                    "jobs": list_jobs,
                    "timeout": _w.timeout,
                    "sync": _w.sync,
                    "type": "test"
                }
                list_work.append(_dt)
    except Exception, e:
        pass

    try:
        _work_data = Configure_Manage_Work_Tag_Data.objects.filter(asset_tag_id__in=list_tag_id, begin=True)
        for _wd in _work_data:
            try:
                if _wd.work.status == 4:
                    try:
                        Configure_Manage_Work_Result_Data.objects.get(work=_wd.work, asset=asset)
                    except Exception, e:
                        list_jobs = []
                        jobs = _wd.work.jobs
                        if not isinstance(jobs, list):
                            jobs = json.loads(jobs)
                        for j in jobs:
                            if not isinstance(j, dict):
                                j = json.loads(j)
                            if j['type'] == 'command':
                                job_now = Remote_Control_Command.objects.get(id=j['id'])
                                _dtt = {
                                    "id": job_now.id,
                                    "ignore_error": j['ignore_error'],
                                    "desc": job_now.desc,
                                    "command": job_now.command,
                                    "type": "command",
                                }
                            elif j['type'] == 'script':
                                job_now = Remote_Control_Script.objects.get(id=j['id'])
                                _dtt = {
                                    "id": job_now.id,
                                    "ignore_error": j['ignore_error'],
                                    "desc": job_now.desc,
                                    "args": j['args'],
                                    "script": open(job_now.script, 'r').readlines(),
                                    "type": "script",
                                    "md5": hashlib.md5(open(job_now.script, 'rb').read()).hexdigest(),
                                }
                            elif j['type'] == 'copy':
                                job_now = Remote_Control_Copy.objects.get(id=j['id'])
                                _dtt = {
                                    "id": job_now.id,
                                    "ignore_error": j['ignore_error'],
                                    "desc": job_now.desc,
                                    "dest": j['dest'],
                                    "authority": j['authority'],
                                    "src": base64.b64encode(open(job_now.src, 'rb').read()),
                                    "type": "copy",
                                    "check_change": j['check_change'],
                                    "md5": hashlib.md5(open(job_now.src, 'rb').read()).hexdigest(),
                                }
                            list_jobs.append(_dtt)
                        _dt = {
                            "id": _wd.work.id,
                            "name_cn": _wd.work.name_cn,
                            "name_en": _wd.work.name_en,
                            "desc": _wd.work.desc,
                            "jobs": list_jobs,
                            "timeout": _wd.work.timeout,
                            "sync": _wd.work.sync,
                            "type": "online"
                        }
                        list_work.append(_dt)
            except Exception, e:
                continue
    except Exception, e:
        pass
    response_data = {
        "success": True,
        "msg": u"获取作业成功",
        "data": list_work
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def remote_control_query_copy(request):
    """ 配置管理作业查询"""
    id = request.POST.get('id', '')
    if id:
        try:
            db_copy = Remote_Control_Copy.objects.get(id=id)
        except Exception, e:
            response_data = {
                'success': False,
                'msg': u"动作不存在",
                'data': {}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")
        data = {
            'id': id,
            'desc': db_copy.desc,
            'src': db_copy.src,
            'authority': db_copy.authority,
            'dest': db_copy.dest,
            'src_url': db_copy.src_url,
            'src_username': db_copy.src_username,
            'src_password': db_copy.src_password,

        }
        response_data = {
            'success': True,
            'msg': u"查询动作成功",
            'data': data
        }
    else:
        response_data = {
            'success': False,
            'msg': u"查询动作失败",
            'data': {}
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def work_manage_modify(request):
    """ 配置管理作业修改"""
    id = request.GET.get('id', '')
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    list_command = list()
    command = Remote_Control_Command.objects.all()
    for c in command:
        _dt = {
            "command": c.command,
            "desc": c.desc,
            "id": c.id
        }
        list_command.append(_dt)
    argv_local['LIST_COMMAND'] = list_command
    list_script = list()
    script = Remote_Control_Script.objects.all()
    for c in script:
        _dt = {
            "command": c.script,
            "desc": c.desc,
            "args": c.args,
            "id": c.id
        }
        list_script.append(_dt)
    argv_local['LIST_SCRIPT'] = list_script
    list_copy = list()
    copy = Remote_Control_Copy.objects.all()
    for c in copy:
        _dt = {
            "desc": c.desc,
            "id": c.id
        }
        list_copy.append(_dt)
    argv_local['LIST_COPY'] = list_copy
    list_tag = list()
    _asset_tag = Asset_Tag.objects.filter(ontree=False)
    _dt = dict()
    for _at in _asset_tag:
        _dt['id'] = _at.id
        _dt['name'] = _at.name
        list_tag.append(_dt)
        _dt = dict()
    argv_local['LIST_TAG'] = list_tag
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
    except Exception, e:
        return render_to_response('work_manage/add.html', argv_local)
    work = {
        "name_cn": _configure_manage_work.name_cn,
        "name_en": _configure_manage_work.name_en,
        "desc": _configure_manage_work.desc,
        "jobs": json.loads(_configure_manage_work.jobs),
        "test_tag": {
            "id": _configure_manage_work.test_tag.id,
            "name": _configure_manage_work.test_tag.name,
        },
        "timeout": _configure_manage_work.timeout,
        "sync": _configure_manage_work.sync,
        "status": _configure_manage_work.status,
    }
    list_tags = list()
    for t in _configure_manage_work.tags.all():
        _dt = {
            "id": t.id,
            "name": t.name,
        }
        list_tags.append(_dt)
    work['tags'] = list_tags
    argv_local['WORK'] = json.dumps(work)
    return render_to_response('work_manage/modify.html', argv_local)


def work_status_refresh(id, tag=True):
    """ 更新作业状态"""
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
        if tag:
            msg = u"作业:%s正在更新状态" % (_configure_manage_work.name_cn)
            logger = logging.getLogger('log_file')
            logger.info(msg)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.info(msg)
        result_summary = {
            "test": {
                "success": {},
                "failed": {},
                "unknown": {}
            },
            "online": {
                "success": {},
                "failed": {},
                "unknown": {}
            }
        }
        try:
            _asset = _configure_manage_work.test_tag.asset.all()
            for a in _asset:
                result_summary['test']['unknown'][a.id] = {
                    "hostname": a.name,
                    "sn": a.sn,
                }
                try:
                    _work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work=_configure_manage_work, asset=a)
                    for wrd in _work_result_data:
                        if wrd.result.type == 'test':
                            if wrd.result.success:
                                result_summary['test']['success'][a.id] = {
                                    "hostname": a.name,
                                    "sn": a.sn,
                                    "result": wrd.result.data,
                                }
                                del result_summary['test']['unknown'][a.id]
                            else:
                                result_summary['test']['failed'][a.id] = {
                                    "hostname": a.name,
                                    "sn": a.sn,
                                    "result": wrd.result.data,
                                }
                                del result_summary['test']['unknown'][a.id]
                except Exception, e:
                    pass
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"测试tag未绑定资产",
                'data': None
            }
            return json_response_data

        try:
            _asset_tag = _configure_manage_work.tags.all()
            for at in _asset_tag:
                _asset = at.asset.all()
                for a in _asset:
                    result_summary['online']['unknown'][a.id] = {
                        "hostname": a.name,
                        "sn": a.sn,
                    }
                    try:
                        _work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work=_configure_manage_work, asset=a)
                        for wrd in _work_result_data:
                            if wrd.result.type == 'online':
                                if wrd.result.success:
                                    result_summary['online']['success'][a.id] = {
                                        "hostname": a.name,
                                        "sn": a.sn,
                                        "result": wrd.result.data,
                                    }
                                    del result_summary['online']['unknown'][a.id]
                                else:
                                    result_summary['online']['failed'][a.id] = {
                                        "hostname": a.name,
                                        "sn": a.sn,
                                        "result": wrd.result.data,
                                    }
                                    del result_summary['online']['unknown'][a.id]
                    except Exception, e:
                        pass
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"上线tag异常",
                'data': None
            }
            return json_response_data
        if _configure_manage_work.status <= 3:
            num_asset_unknown = len(result_summary['test']['unknown'])
            num_asset_success = len(result_summary['test']['success'])
            num_asset_failed = len(result_summary['test']['failed'])
            msg_tail = u"成功：%d,失败：%d,未知：%d" % (num_asset_success, num_asset_failed, num_asset_unknown)
            if num_asset_failed == 0 and num_asset_unknown == 0:
                msg = u"【测试成功】%s" % msg_tail
                success = True
                _configure_manage_work.status = 2
            elif num_asset_failed != 0:
                msg = u"【测试失败】%s" % msg_tail
                success = False
                _configure_manage_work.status = 3
            else:
                msg = u"%s" % msg_tail
                success = True
        else:
            num_asset_unknown = len(result_summary['online']['unknown'])
            num_asset_success = len(result_summary['online']['success'])
            num_asset_failed = len(result_summary['online']['failed'])
            msg_tail = u"成功：%d,失败：%d,未知：%d" % (num_asset_success, num_asset_failed, num_asset_unknown)
            if num_asset_failed == 0 and num_asset_unknown == 0:
                msg = u"【执行成功】%s" % msg_tail
                success = True
                _configure_manage_work.status = 5
            elif num_asset_failed != 0:
                msg = u"【执行失败】%s" % msg_tail
                success = False
                _configure_manage_work.status = 6
            else:
                msg = u"%s" % msg_tail
                success = True
        if tag:
            msg = u"作业:%s更新状态完毕" % (_configure_manage_work.name_cn)
            logger = logging.getLogger('log_file')
            logger.info(msg)
            if C.LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.info(msg)
            _configure_manage_work.save()
        data = {
            "id": id,
            "status": _configure_manage_work.status,
            "num_asset_unknown": num_asset_unknown,
            "num_asset_success": num_asset_success,
            "num_asset_failed": num_asset_failed,
            "result_summary": result_summary
        }
        json_response_data = {
            "success": success,
            "msg": msg,
            'data': data
        }
        return json_response_data
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"更新失败",
            'data': None
        }
        return json_response_data


@login_required
@csrf_exempt
def configure_manage_work_status_refresh(request):
    """ 配置管理作业更新状态"""
    id = request.POST.get('id', '')
    json_response_data = work_status_refresh(id, tag=False)
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@login_required
@csrf_exempt
def work_manage_status_detail(request):
    """ 作业管理结果详情查询"""
    id = request.GET.get('id', '')
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    argv_local['RESULT_DETAIL'] = work_status_refresh(id, tag=False)
    argv_local['STR_RESULT_DETAIL'] = json.dumps(argv_local['RESULT_DETAIL'])
    return render_to_response('work_manage/status_detail.html', argv_local)


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_delete(request):
    """ 作业删除 """
    id = request.POST.get('id', '')
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
        _configure_manage_task_data = _configure_manage_work.Configure_Manage_Task_Data.all()
        if _configure_manage_task_data:
            json_response_data = {
                "success": False,
                "msg": u"该作业存在绑定任务",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        _configure_manage_work.delete()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"作业已经不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"删除作业成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_query_status_detail(request):
    id = request.POST.get('id', '')
    timestamp = request.POST.get('timestamp', 0)
    if not isinstance(timestamp, float):
        try:
            timestamp = float(timestamp)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"参数不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    timestamp_server = timestamp
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"作业不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    list_msg = [u"未进行", u"测试中", u"测试成功", u"测试失败", u"执行中", u"执行成功", u"执行失败", u"忽略测试失败", u"忽略执行失败"]
    if _configure_manage_work.status != 1 and _configure_manage_work.status != 4:
        end = {
            "tag": True,
            "status": _configure_manage_work.status,
            "msg": list_msg[_configure_manage_work.status]
        }
    else:
        end = {
            "tag": False,
            "status": _configure_manage_work.status,
            "msg": list_msg[_configure_manage_work.status]
        }
    data = list()
    configure_manage_work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work=_configure_manage_work)
    for c_m_w_r_d in configure_manage_work_result_data:
        timestamp_server = time.mktime(c_m_w_r_d.result.modtime.timetuple())
        if timestamp_server > timestamp:
            _dt = {
                'agent': c_m_w_r_d.asset.name,
                'msg': u"执行成功" if c_m_w_r_d.result.success else u"执行失败",
                'work_name': c_m_w_r_d.work.name_cn,
            }
            data.append(_dt)
    json_response_data = {
        "success": True,
        "msg": u"更新作业状态成功",
        "end": end,
        'data': data,
        'timestamp': float(timestamp_server)
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_query_status(request):
    id = request.POST.get('id', '')
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"作业不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    list_msg = [u"未进行", u"测试中", u"测试成功", u"测试失败", u"执行中", u"执行成功", u"执行失败", u"忽略测试失败", u"忽略执行失败"]
    data = {
        "status": _configure_manage_work.status,
        "msg": list_msg[_configure_manage_work.status]
    }
    json_response_data = {
        "success": True,
        "msg": u"更新作业状态成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_work_online(request):
    """ 配置管理作业上线"""
    id = request.POST.get('id', '')
    try:
        _configure_manage_work = Configure_Manage_Work.objects.get(id=id)
        if not check_task_status_from_work(_configure_manage_work):
            json_response_data = {
                "success": False,
                "msg": u"作业锁定中",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        if _configure_manage_work.status == 2:
            _configure_manage_work.status = 4
            _configure_manage_work.save()
            list_tag_data = _configure_manage_work.Configure_Manage_Work_Tag_Data.all()
            try:
                work_tag_data = _configure_manage_work.Configure_Manage_Work_Tag_Data.get(begin=True)
            except Exception, e:
                work_tag_data = list_tag_data[0]
                work_tag_data.begin = True
                work_tag_data.save()
            try:
                _configure_manage_work.result.filter(type='online').delete()
            except Exception, e:
                pass
        else:
            json_response_data = {
                "success": False,
                "msg": u"作业尚未通过测试",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    except Exception,e:
        json_response_data = {
            "success": False,
            "msg": u"作业不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"上线作业开始",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_save(request):
    """ 新增任务"""
    name_cn = request.POST.get('name_cn', '')
    name_en = request.POST.get('name_en', '')
    desc = request.POST.get('desc', '')
    time_auto_exec = request.POST.get('time_auto_exec', '')
    string_works = request.POST.get('works', '')
    if time_auto_exec:
        time_auto_exec = datetime.datetime.fromtimestamp(time.mktime(time.strptime(time_auto_exec, "%Y-%m-%d %H:%M")))
    else:
        time_auto_exec = datetime.datetime.fromtimestamp(time.mktime(time.strptime('1970-1-1 08:00', "%Y-%m-%d %H:%M")))
    try:
        list_work_id = eval(string_works)
    except Exception, e:
        try:
            list_work_id = json.loads(str(string_works))
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"参数不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(name_en=name_en)
        _configure_manage_task.name_cn = name_cn
        _configure_manage_task.desc = desc
        _configure_manage_task.time_auto_exec = time_auto_exec
        _configure_manage_task.save()
    except Exception, e:
        _configure_manage_task = Configure_Manage_Task(name_cn=name_cn, name_en=name_en, desc=desc, time_auto_exec=time_auto_exec)
        _configure_manage_task.save()

    for lwi in list_work_id:
        # 暂时注释忘记为什么之前会限制一个作业只能绑定一个任务
        # _configure_manage_task_data = Configure_Manage_Task_Data.objects.filter(work_id=lwi['id']).exclude(task=_configure_manage_task)
        # if _configure_manage_task_data:
        #     _configure_manage_work = Configure_Manage_Work.objects.get(id=lwi['id'])
        #     json_response_data = {
        #         "success": False,
        #         "msg": u"作业:%s已存在绑定任务" % _configure_manage_work.name_cn,
        #         'data': {
        #             "id": _configure_manage_task.id
        #         }
        #     }
        #     return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        # else:
        try:
            _configure_manage_task_data = Configure_Manage_Task_Data.objects.get(work_id=lwi['id'], task=_configure_manage_task)
            _configure_manage_task_data.check_true = lwi['check_true']
            _configure_manage_task_data.save()
        except Exception, e:
            _configure_manage_task_data = Configure_Manage_Task_Data(work_id=lwi['id'], task=_configure_manage_task, check_true=lwi['check_true'])
            _configure_manage_task_data.save()

    json_response_data = {
        "success": True,
        "msg": u"任务保存成功",
        'data': {
            "id": _configure_manage_task.id
        }
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_test(request):
    """ 配置管理任务测试"""
    id = request.POST.get('id', '')
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
        _configure_manage_task.status = 1
        _configure_manage_task.save()
        try:
            works = _configure_manage_task.work.all()
            for w in works:
                jobs = w.jobs
                if not isinstance(jobs, list):
                    jobs = json.loads(jobs)
                for j in jobs:
                    if not isinstance(j, dict):
                        j = json.loads(j)
                    if j['type'] == 'copy':
                        remote_control_copy = Remote_Control_Copy.objects.get(id=int(j['id']))
                        if remote_control_copy.src_url:
                            if remote_control_copy.src_username or remote_control_copy.src_password:
                                with_pass = True
                            else:
                                with_pass = False
                            re = download_file(remote_control_copy.src_url, remote_control_copy.src, with_pass,
                                               remote_control_copy.src_username, remote_control_copy.src_password)
                            if not re['success'] and not j['ignore_error']:
                                return HttpResponse(json.dumps(re), content_type="application/json; charset=utf-8")
                w.status = 1
                w.save()
                w.result.all().delete()
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"任务异常",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    except Exception,e:
        json_response_data = {
            "success": False,
            "msg": u"任务不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"测试任务开始",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_query_status_detail(request):
    id = request.POST.get('id', '')
    timestamp = request.POST.get('timestamp', 0)
    if not isinstance(timestamp, float):
        try:
            timestamp = float(timestamp)
        except Exception, e:
            json_response_data = {
                "success": False,
                "msg": u"参数不合法",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    timestamp_server = timestamp
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"任务不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    list_msg = [u"未进行", u"测试中", u"测试成功", u"测试失败", u"执行中", u"执行成功", u"执行失败", u"忽略测试失败", u"忽略执行失败"]
    if _configure_manage_task.status != 1 and _configure_manage_task.status != 4:
        end = {
            "tag": True,
            "status": _configure_manage_task.status,
            "msg": list_msg[_configure_manage_task.status]
        }
    else:
        end = {
            "tag": False,
            "status": _configure_manage_task.status,
            "msg": list_msg[_configure_manage_task.status]
        }
    data = list()
    _configure_manage_work = _configure_manage_task.work.all()
    configure_manage_work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work__in=_configure_manage_work)
    for c_m_w_r_d in configure_manage_work_result_data:
        timestamp_server = time.mktime(c_m_w_r_d.result.modtime.timetuple())
        if timestamp_server > timestamp:
            _dt = {
                'agent': c_m_w_r_d.asset.name,
                'msg': u"执行成功" if c_m_w_r_d.result.success else u"执行失败",
                'work_name': c_m_w_r_d.work.name_cn,
            }
            data.append(_dt)
    json_response_data = {
        "success": True,
        "msg": u"更新作业状态成功",
        "end": end,
        'data': data,
        'timestamp': float(timestamp_server)
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_query_status(request):
    id = request.POST.get('id', '')
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"任务不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    list_msg = [u"未进行", u"测试中", u"测试成功", u"测试失败", u"执行中", u"执行成功", u"执行失败", u"忽略测试失败", u"忽略执行失败"]
    data = {
        "status": _configure_manage_task.status,
        "msg": list_msg[_configure_manage_task.status]
    }
    json_response_data = {
        "success": True,
        "msg": u"更新任务状态成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_online(request):
    """ 配置管理任务上线"""
    id = request.POST.get('id', '')
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
        if _configure_manage_task.status == 2:
            _configure_manage_task.status = 4
            _configure_manage_task.time_auto_exec = datetime.datetime.fromtimestamp(time.mktime(time.strptime('1970-1-1 08:00', "%Y-%m-%d %H:%M")))
            _configure_manage_task.save()
            configure_manage_task_data = Configure_Manage_Task_Data.objects.filter(task=_configure_manage_task)
            tag = False
            for c_m_t_d in configure_manage_task_data:
                if c_m_t_d.check_true:
                    tag = True
                if not tag:
                    if c_m_t_d.work.status == 2:
                        c_m_t_d.work.status = 4
                        c_m_t_d.work.save()
                    else:
                        json_response_data = {
                            "success": False,
                            "msg": u"作业%s尚未通过测试" % c_m_t_d.work.name_cn,
                            'data': None
                        }
                        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
                    list_tag_data = Configure_Manage_Work_Tag_Data.objects.filter(work=c_m_t_d.work)
                    try:
                        work_tag_data = Configure_Manage_Work_Tag_Data.objects.get(begin=True, work=c_m_t_d.work)
                    except Exception, e:
                        work_tag_data = list_tag_data[0]
                        work_tag_data.begin = True
                        work_tag_data.save()
                else:
                    tag = False

            try:
                works = _configure_manage_task.work.all()
                for w in works:
                    w.result.filter(type='online').delete()
            except Exception, e:
                pass
        else:
            json_response_data = {
                "success": False,
                "msg": u"任务尚未通过测试",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    except Exception,e:
        json_response_data = {
            "success": False,
            "msg": u"任务不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"任务作业开始",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_delete(request):
    """ 任务删除 """
    id = request.POST.get('id', '')
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
        _configure_manage_task.delete()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"任务已经不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"删除任务成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def configure_manage_task_continue(request):
    """ 任务删除 """
    id = request.POST.get('id', '')
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
        _configure_manage_work = _configure_manage_task.work.all()
        for c_m_w in _configure_manage_work:
            if c_m_w.status == 3:
                c_m_w.status = 7
                c_m_w.save()
            elif c_m_w.status == 6:
                c_m_w.status = 8
                c_m_w.save()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"任务无法继续",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    data = {
        "id": id
    }
    json_response_data = {
        "success": True,
        "msg": u"继续任务成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def task_manage_modify(request):
    """ 配置管理任务修改"""
    id = request.GET.get('id', '')
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    _work = Configure_Manage_Work.objects.all()
    list_work = list()
    for w in _work:
        _dt = {
            "id": w.id,
            "name_en": w.name_en,
            "name_cn": w.name_cn,
            "status": w.status,
        }
        list_work.append(_dt)
    argv_local['LIST_WORK'] = list_work
    try:
        _configure_manage_task = Configure_Manage_Task.objects.get(id=id)
    except Exception, e:
        return render_to_response('task_manage/add.html', argv_local)
    _task = {
        "name_cn": _configure_manage_task.name_cn,
        "name_en": _configure_manage_task.name_en,
        "desc": _configure_manage_task.desc,
        "time_auto_exec": time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(_configure_manage_task.time_auto_exec.timetuple()) + 8 * 60 * 60 )),
        "status": _configure_manage_task.status,
        "works": []
    }
    configure_manage_task_data = Configure_Manage_Task_Data.objects.filter(task=_configure_manage_task)
    for c_m_t_d in configure_manage_task_data:
        _dt = {
            "id": c_m_t_d.work.id,
            "name": c_m_t_d.work.name_cn,
            "check_true": c_m_t_d.check_true
        }
        _task['works'].append(_dt)
    argv_local['TASK'] = json.dumps(_task)
    return render_to_response('task_manage/modify.html', argv_local)


@login_required
@csrf_exempt
def task_manage_status_detail(request):
    """ 任务管理详情查询"""
    id = request.GET.get('id', '')
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    try:
        _work = Configure_Manage_Task.objects.get(id=id).work.all()
    except Exception, e:
        _work = []
    list_work = list()
    for w in _work:
        _dt = {
            "id": w.id,
            "name_en": w.name_en,
            "name_cn": w.name_cn,
            "status": w.status,
        }
        list_work.append(_dt)
    argv_local['LIST_WORK'] = list_work
    return render_to_response('task_manage/status_detail.html', argv_local)


@login_required
@csrf_exempt
def bussiness_manage(request):
    """ 业务管理 """
    argv_local = dict()
    argv_local['USER'] = request.user.username
    return render_to_response('bussiness_manage/bussiness_manage.html', argv_local)


@login_required
@csrf_exempt
def bussiness_manage_index(request):
    """ 业务管理主页 """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    list_bussiness = list()
    user = request.user
    authority_bussiness = Authority_Bussiness.objects.filter(user=user)
    for a_b in authority_bussiness:
        dt = {
            'id': a_b.bussiness.id,
            'name_en': a_b.bussiness.name_en,
            'name_cn': a_b.bussiness.name_cn,
            'creator': User.objects.get(id=a_b.bussiness.creator_id).username,
        }
        list_bussiness.append(dt)
    argv_local['LIST_BUSSINESS'] = list_bussiness
    return render_to_response('bussiness_manage/index.html', argv_local)


@csrf_exempt
@login_required
@authority_url
def bussiness_manage_add(request):
    """ 新增业务 """
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    list_work = list()
    configure_manage_work = Configure_Manage_Work.objects.all()
    for c_m_w in configure_manage_work:
        dt = {
            'id': c_m_w.id,
            'name_cn': c_m_w.name_cn
        }
        list_work.append(dt)
    argv_local['LIST_WORK'] = list_work

    list_task = list()
    configure_manage_task = Configure_Manage_Task.objects.all()
    for c_m_t in configure_manage_task:
        dt = {
            'id': c_m_t.id,
            'name_cn': c_m_t.name_cn
        }
        list_task.append(dt)
    argv_local['LIST_TASK'] = list_task

    list_user = list()
    user = User.objects.all()
    for u in user:
        dt = {
            'id': u.id,
            'name': u.username
        }
        list_user.append(dt)
    argv_local['LIST_USER'] = list_user

    return render_to_response('bussiness_manage/add.html', argv_local)

@csrf_exempt
@login_required
@authority_url
def bussiness_manage_save(request):
    name_cn = request.POST.get('name_cn', '')
    name_en = request.POST.get('name_en', '')
    desc = request.POST.get('desc', '')
    creator = request.user
    try:
        bussiness = Bussiness.objects.get(name_en=name_en)
        bussiness.name_cn = name_cn
        bussiness.desc = desc
    except Exception, e:
        bussiness = Bussiness(name_cn=name_cn, name_en=name_en, desc=desc, creator=creator)
    try:
        bussiness.save()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"保存业务失败",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    try:
        Authority_Bussiness.objects.get(bussiness=bussiness, user=creator)
    except Exception, e:
        authority_bussiness = Authority_Bussiness(bussiness=bussiness, user=creator)
        authority_bussiness.save()

    json_response_data = {
        "success": True,
        "msg": u"保存业务成功",
        'data': {'id': bussiness.id}
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def bussiness_manage_add_btn(request):
    bussiness_id = request.POST.get('bussiness_id', '')
    name = request.POST.get('name', '')
    work_id = request.POST.get('work_id', '')
    task_id = request.POST.get('task_id', '')
    type = request.POST.get('type', '')
    if type == 'work' and work_id != '' and work_id:
        data = {
            'type': type,
            'id': work_id,
            'name': name
        }
        try:
            bussiness_btn = Bussiness_Btn.objects.get(name=name, bussiness_id=bussiness_id)
            bussiness_btn.work_id = work_id
            bussiness_btn.type = type
        except Exception, e:
            bussiness_btn = Bussiness_Btn(name=name, bussiness_id=bussiness_id, work_id=work_id, type=type)

    elif type == 'task' and task_id != '' and task_id:
        data = {
            'type': type,
            'id': task_id,
            'name': name
        }
        try:
            bussiness_btn = Bussiness_Btn.objects.get(name=name, bussiness_id=bussiness_id)
            bussiness_btn.task_id = task_id
            bussiness_btn.type = type
        except Exception, e:
            bussiness_btn = Bussiness_Btn(name=name, bussiness_id=bussiness_id, task_id=task_id, type=type)
    else:
        json_response_data = {
            "success": False,
            "msg": u"添加按钮失败,参数不合法",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    try:
        bussiness_btn.save()
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"添加按钮失败",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")

    json_response_data = {
        "success": True,
        "msg": u"添加按钮成功",
        'data': data
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def bussiness_manage_add_person(request):
    bussiness_id = request.POST.get('bussiness_id', '')
    user_id = request.POST.get('user_id', '')
    if user_id != '' and bussiness_id != '':
        try:
            Authority_Bussiness.objects.get(user_id=user_id, bussiness_id=bussiness_id)
            json_response_data = {
                "success": False,
                "msg": u"负责人已存在",
                'data': None
            }
            return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
        except Exception, e:
            authority_bussiness = Authority_Bussiness(user_id=user_id, bussiness_id=bussiness_id)
            authority_bussiness.save()
    else:
        json_response_data = {
            "success": False,
            "msg": u"添加负责人失败,参数不合法",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    json_response_data = {
        "success": True,
        "msg": u"添加负责人成功",
        'data': {'username': User.objects.get(id=user_id).username}
    }
    return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")


@csrf_exempt
@login_required
@authority_url
def bussiness_manage_bussiness_detail(request):
    bussiness_id = request.GET.get('id', '')
    try:
        bussiness = Bussiness.objects.get(id=bussiness_id)
    except Exception, e:
        json_response_data = {
            "success": False,
            "msg": u"业务不存在",
            'data': None
        }
        return HttpResponse(json.dumps(json_response_data), content_type="application/json; charset=utf-8")
    argv_local = dict()
    argv_local['BODY_BG'] = 'white-bg'
    argv_local['BUSSINESS'] = json.dumps({
        'id': bussiness.id,
        'name_cn': bussiness.name_cn,
        'name_en': bussiness.name_en,
        'desc': bussiness.desc,
    })
    list_work = list()
    configure_manage_work = Configure_Manage_Work.objects.all()
    for c_m_w in configure_manage_work:
        dt = {
            'id': c_m_w.id,
            'name_cn': c_m_w.name_cn
        }
        list_work.append(dt)
    argv_local['LIST_WORK'] = list_work

    list_task = list()
    configure_manage_task = Configure_Manage_Task.objects.all()
    for c_m_t in configure_manage_task:
        dt = {
            'id': c_m_t.id,
            'name_cn': c_m_t.name_cn
        }
        list_task.append(dt)
    argv_local['LIST_TASK'] = list_task

    list_user = list()
    user = User.objects.all()
    for u in user:
        dt = {
            'id': u.id,
            'name': u.username
        }
        list_user.append(dt)
    argv_local['LIST_USER'] = list_user

    list_btn = list()
    bussiness_btns = bussiness.Bussiness_Btns.all()
    for b_b in bussiness_btns:
        if b_b.type == 'work':
            dt = {
                'id': b_b.work_id,
                'type': b_b.type,
                'name': b_b.name
            }
        else:
            dt = {
                'id': b_b.task_id,
                'type': b_b.type,
                'name': b_b.name
            }
        list_btn.append(dt)
    argv_local['LIST_BTN'] = list_btn

    list_person = list()
    authority_bussiness = Authority_Bussiness.objects.filter(bussiness=bussiness)
    for a_b in authority_bussiness:
        dt = {
            'username': User.objects.get(id=a_b.user_id).username
        }
        list_person.append(dt)
    argv_local['LIST_PERSON'] = list_person
    return render_to_response('bussiness_manage/detail.html', argv_local)