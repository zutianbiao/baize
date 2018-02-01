#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统负责生成随机密码的api接口


###################################################################################################
import string
from random import choice


def fun_generate_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])