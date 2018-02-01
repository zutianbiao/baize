#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django models配置文件
# 生产迁移记录 /usr/local/baize/env/bin/python manage.py makemigrations
# 生产数据库 /usr/local/baize/env/bin/python manage.py migrate --database=proxy


###################################################################################################
from django.db import models


class Config_Items(models.Model):
    """ 配置项数据表 """
    item_name = models.CharField(max_length=128, blank=False, null=False)
    item_value = models.CharField(max_length=1024, blank=False, null=False)
    group_name = models.CharField(max_length=1024, blank=False, null=False)
    desc = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = 'APP_proxy'
        db_table = 'tb_config_items'
        unique_together = ('item_name', 'group_name')

    def __unicode__(self):
        return self.item_name

