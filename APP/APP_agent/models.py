#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django models配置文件
# 生产迁移记录 /usr/local/baize/env/bin/python manage.py makemigrations
# 生产数据库 /usr/local/baize/env/bin/python manage.py migrate --database=agent


###################################################################################################
from django.db import models


class Config_Items(models.Model):
    """ 配置项数据表 """
    item_name = models.CharField(max_length=128, blank=False, null=False)
    item_value = models.CharField(max_length=1024, blank=False, null=False)
    group_name = models.CharField(max_length=1024, blank=False, null=False)
    desc = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = 'APP_agent'
        db_table = 'tb_config_items'
        unique_together = ('item_name', 'group_name')

    def __unicode__(self):
        return self.item_name


class Proxy_Server(models.Model):
    """ 配置项数据表 """
    ip = models.IPAddressField(blank=False, null=False, default='127.0.0.1')
    port = models.IntegerField(blank=False, null=False, default=8101)
    speed = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'APP_agent'
        db_table = 'tb_proxy_server'
        unique_together = ('ip', 'port')

    def __unicode__(self):
        return self.id


class Configure_Manage_Work(models.Model):
    """ 作业管理任务表 """
    name_cn = models.CharField(max_length=256, blank=True, null=True)
    name_en = models.CharField(max_length=32, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    jobs = models.TextField(blank=False, null=False)
    timeout = models.IntegerField(help_text=u'超时时间,单位分钟', blank=False, null=False, default=1)
    sync = models.BooleanField(default=True)
    type = models.CharField(max_length=32, blank=False, null=False)
    status = models.IntegerField(help_text=u'当前状态,0未进行，1测试中，2测试成功，3测试失败，4执行中，5执行成功，6执行失败', blank=False, null=False, default=0)
    result = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'APP_agent'
        db_table = 'tb_configure_manage_work'

    def __unicode__(self):
        return self.id