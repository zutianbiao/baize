#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,是Baize的数据库路由文件


###################################################################################################


class App_Router(object):
    """
    基于App的DB Router
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['APP_web', 'APP_master', 'APP_proxy', 'APP_agent', 'APP_demo']:
            return model._meta.app_label.replace('APP_', '')
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['APP_web', 'APP_master', 'APP_proxy', 'APP_agent', 'APP_demo']:
            return model._meta.app_label.replace('APP_', '')
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, model):
        # 自定义app与default不要重复迁移
        if db in ['web', 'master', 'proxy', 'agent', 'demo']:
            return model._meta.app_label == "APP_%s" % db
        elif model._meta.app_label in ['APP_web', 'APP_master', 'APP_proxy', 'APP_agent', 'APP_demo']:
            return False
        return True