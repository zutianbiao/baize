#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统负责读取配置项的API接口


###################################################################################################
import logging
from baize.settings import *
from APP.APP_web.models import Config_Items


class Config(object):
    """ 配置项管理类 """
    def __init__(self):
        pass

    def add_item(self, item_name=None, group_name=None, item_value=None):
        """ 添加配置项,如果已经存在则进行更新 """
        if self.item(item_name=item_name, group_name=group_name):
            re = self.del_item(item_name=item_name, group_name=group_name)
            if isinstance(re, tuple):
                raise re[1]
        _cf_item = Config_Items(item_name=item_name, group_name=group_name, item_value=item_value)
        _cf_item.save()

    def del_item(self, item_name=None, group_name=None):
        """ 删除配置项 """
        if not item_name:
            return False
        if not group_name:
            return False
        try:
            re = Config_Items.objects.filter(item_name=item_name, group_name=group_name).delete()
            return re
        except Exception, e:
            logger = logging.getLogger('log_file')
            logger.error(e)
            if LOG_SCREEN == 'ON':
                logger = logging.getLogger('log_screen')
                logger.error(e)
            re = False
            return re, e

    def item(self, item_name=None, group_name=None, default=None, type=None):
        """ 查询配置项 """
        if not item_name:
            if type is not None and (isinstance(default, str) or isinstance(default, unicode)):
                return eval(type)(default)
            else:
                return default
        if not group_name:
            if type is not None and (isinstance(default, str) or isinstance(default, unicode)):
                return eval(type)(default)
            else:
                return default
        try:
            re = Config_Items.objects.get(item_name=item_name, group_name=group_name).item_value
        except Exception, e:
            if default is not None:
                _config_items = Config_Items(item_name=item_name, group_name=group_name, item_value=default)
                _config_items.save()
            re = default
        if type is not None and (isinstance(re, str) or isinstance(re, unicode)):
            return eval(type)(re)
        else:
            return re