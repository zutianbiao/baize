#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的django models配置文件
# 生产迁移记录 /usr/local/baize/env/bin/python manage.py makemigrations
# 生产数据库 /usr/local/baize/env/bin/python manage.py migrate --database=web


###################################################################################################
from django.db import models
from django.contrib.auth.models import User


class Config_Items(models.Model):
    """ 配置项数据表 """
    item_name = models.CharField(max_length=128, blank=False, null=False)
    item_value = models.CharField(max_length=1024, blank=False, null=False)
    group_name = models.CharField(max_length=24, blank=False, null=False)
    desc = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_config_items'
        unique_together = ('item_name', 'group_name')

    def __unicode__(self):
        return self.item_name


class Dict(models.Model):
    """ 字典表 """
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    key = models.CharField(max_length=32, blank=False, null=False)
    value = models.CharField(max_length=128, blank=False, null=False)
    desc = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_dict'

    def __unicode__(self):
        return self.name


class Property_Template(models.Model):
    name = models.CharField(max_length=32, help_text=u'属性名称', blank=False, null=False, unique=True)
    desc = models.CharField(max_length=256, help_text=u'描述', blank=True, null=True)
    type = models.CharField(max_length=32, blank=False, null=False)
    steps = models.IntegerField(help_text=u'属性抓取周期,单位分钟', blank=True, null=True)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间', blank=False, null=False)
    reciver = models.CharField(max_length=32, blank=False, null=False)
    save_method = models.IntegerField(help_text=u'属性存储方法', blank=False, null=False, default=0)  # 0覆盖 1变更追加


    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_property_template'

    def __unicode__(self):
        return self.name


class Property(models.Model):
    property_template = models.ForeignKey(Property_Template, related_name='Property', to_field='name', on_delete=models.CASCADE, blank=False, null=False)
    value = models.TextField(blank=True, null=True)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间', blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_property'

    def __unicode__(self):
        return self.value


class Module_Template(models.Model):
    name = models.CharField(max_length=32, help_text=u'模块名称', blank=False, null=False, unique=True)
    desc = models.CharField(max_length=256, help_text=u'描述', blank=True, null=True)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')
    property_template = models.ManyToManyField(Property_Template, through='Module_Template_Data', blank=True, null=True, help_text=u'该模块包含的属性')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_module_template'

    def __unicode__(self):
        return self.name


class Module_Template_Data(models.Model):
    property = models.ForeignKey(Property_Template, related_name='Module_Template_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)
    module = models.ForeignKey(Module_Template, related_name='Module_Template_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_module_template_data'

    def __unicode__(self):
        return str(self.id)


class Asset_Template(models.Model):
    name = models.CharField(max_length=32, help_text=u'资产模板名称', blank=False, null=False, unique=True)
    desc = models.CharField(max_length=256, help_text=u'描述', blank=True, null=True)
    property = models.ManyToManyField(Property_Template, through='Asset_Template_Data', blank=True, null=True, help_text=u'该资产模板包含的属性')
    module = models.ManyToManyField(Module_Template, through='Asset_Template_Data', blank=True, null=True, help_text=u'该资产模板包含的模块')
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_template'

    def __unicode__(self):
        return self.name


class Asset_Template_Data(models.Model):
    property = models.ForeignKey(Property_Template, related_name='Asset_Template_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)
    module = models.ForeignKey(Module_Template, related_name='Asset_Template_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)
    asset_template = models.ForeignKey(Asset_Template, related_name='Asset_Template_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_template_data'

    def __unicode__(self):
        return str(self.id)


class Asset(models.Model):
    name = models.CharField(max_length=32, help_text=u'资产名称', blank=False, null=False)
    desc = models.CharField(max_length=256, help_text=u'描述', blank=True, null=True)
    sn = models.CharField(max_length=128, help_text=u'SN', blank=False, null=False)
    property = models.ManyToManyField(Property, through='Asset_Data', help_text=u'该资产包含的属性', blank=True, null=True)
    asset_template = models.ManyToManyField(Asset_Template, through='Asset_Data', help_text=u'该资产对应的资产模板', blank=True, null=True)
    module = models.ManyToManyField(Module_Template, through='Asset_Data', help_text=u'该资产包含的模块', blank=True, null=True)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset'
        unique_together = ('name', 'sn')

    def __unicode__(self):
        return self.name


class Asset_Data(models.Model):
    property = models.ForeignKey(Property, related_name='Asset_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    module = models.ForeignKey(Module_Template, related_name='Asset_Data', to_field='name', on_delete=models.CASCADE, blank=True, null=True)
    asset_template = models.ForeignKey(Asset_Template, related_name='Asset_Data', to_field='name', on_delete=models.CASCADE, blank=True, null=True)
    asset = models.ForeignKey(Asset, related_name='Asset_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_data'

    def __unicode__(self):
        return str(self.id)


class Asset_Group(models.Model):
    name = models.CharField(max_length=32, help_text=u'集群名称', blank=False, null=False, unique=True)
    desc = models.CharField(max_length=256, help_text=u'描述', blank=True, null=True)
    asset = models.ManyToManyField(Asset, through='Asset_Group_Data', blank=True, null=True, help_text=u'该集群包含的主机')
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_group'

    def __unicode__(self):
        return self.name


class Asset_Group_Data(models.Model):
    asset = models.ForeignKey(Asset, related_name='Asset_Group_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    asset_group = models.ForeignKey(Asset_Group, related_name='Asset_Group_Data', to_field='name', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_group_data'

    def __unicode__(self):
        return str(self.id)


class Geo(models.Model):
    """ 地理位置及其经纬度数据库 """
    country = models.CharField(max_length=32, blank=False, null=False)
    province = models.CharField(max_length=32, blank=False, null=False)
    city = models.CharField(max_length=32, blank=True, null=True)
    area = models.CharField(max_length=32, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_geo'
        unique_together = ('country', 'province', 'city', 'area')

    def __unicode__(self):
        return str(self.id)


class Isp(models.Model):
    """ 运营商数据库 """
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_isp'

    def __unicode__(self):
        return str(self.id)


class Detect_Role(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    desc = models.CharField(max_length=128, blank=True, null=True)
    asset = models.ForeignKey(Asset, related_name='Detect_Role', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    target = models.CharField(max_length=64, blank=True, null=True)
    geo = models.ForeignKey(Geo, related_name='Detect_Role', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    isp = models.ForeignKey(Isp, related_name='Detect_Role', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_detect_role'
        unique_together = ('name', 'desc', 'asset', 'target')

    def __unicode__(self):
        return self.name


class Detect_Task(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    desc = models.CharField(max_length=256, blank=True, null=True)


    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_detect_task'

    def __unicode__(self):
        return self.name


class Ping_Detect(models.Model):
    task = models.ForeignKey(Detect_Task, related_name='Ping_Detect', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    source = models.ForeignKey(Detect_Role, related_name='Ping_Detect_As_Source', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    target = models.ForeignKey(Detect_Role, related_name='Ping_Detect_As_Target', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    steps = models.IntegerField(help_text=u'探测周期,单位秒钟', blank=False, null=False, default=60)
    num = models.IntegerField(help_text=u'ping包数目', blank=False, null=False, default=10)
    interval = models.FloatField(help_text=u'ping包时间间隔,单位秒钟', blank=False, null=False, default=0.1)
    timeout = models.IntegerField(help_text=u'ping包超时时间,单位秒钟', blank=False, null=False, default=1)
    size = models.IntegerField(help_text=u'ping包大小,单位B', blank=False, null=False, default=64)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')
    success = models.BooleanField(default=True)
    lost_rate = models.FloatField(blank=True, null=True)
    rtt = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_ping_detect'
        unique_together = ('task', 'source', 'target')

    def __unicode__(self):
        return str(self.id)


class Traceroute_Detect(models.Model):
    task = models.ForeignKey(Detect_Task, related_name='Traceroute_Detect', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    source = models.ForeignKey(Detect_Role, related_name='Traceroute_Detect_As_Source', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    target = models.ForeignKey(Detect_Role, related_name='Traceroute_Detect_As_Target', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    steps = models.IntegerField(help_text=u'探测周期,单位秒钟', blank=False, null=False, default=60)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')
    num = models.IntegerField(help_text=u'traceroute查询包数量', blank=False, null=False, default=1)
    timeout = models.IntegerField(help_text=u'traceroute查询包超时时间,单位秒钟', blank=False, null=False, default=1)
    success = models.BooleanField(default=True)
    data = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_traceroute_detect'
        unique_together = ('task', 'source', 'target')

    def __unicode__(self):
        return str(self.id)


class Curl_Detect(models.Model):
    task = models.ForeignKey(Detect_Task, related_name='Curl_Detect', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    source = models.ForeignKey(Detect_Role, related_name='Curl_Detect_As_Source', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    target = models.ForeignKey(Detect_Role, related_name='Curl_Detect_As_Target', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    uri = models.CharField(max_length=128, blank=True, null=True)
    steps = models.IntegerField(help_text=u'探测周期,单位秒钟', blank=False, null=False, default=300)
    modtime = models.DateTimeField(auto_now=True, help_text=u'最后修改时间')
    timeout_total = models.IntegerField(help_text=u'curl超时时间,单位秒钟', blank=False, null=False, default=300)
    timeout_conn = models.IntegerField(help_text=u'curl建连超时时间,单位秒钟', blank=False, null=False, default=3)
    timeout_dns = models.IntegerField(help_text=u'dns解析超时时间,单位秒钟', blank=False, null=False, default=3)
    success = models.BooleanField(default=True)
    time_conn = models.FloatField(blank=True, null=True)
    time_total = models.FloatField(blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_curl_detect'
        unique_together = ('task', 'source', 'target', 'uri')

    def __unicode__(self):
        return str(self.id)


class Remote_Control_Command(models.Model):
    desc = models.CharField(max_length=256, blank=True, null=True)
    command = models.CharField(max_length=128, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_remote_control_command'

    def __unicode__(self):
        return str(self.id)


class Remote_Control_Script(models.Model):
    desc = models.CharField(max_length=128, blank=False, null=False, unique=True)
    script = models.CharField(max_length=256, blank=False, null=False)
    args = models.BooleanField(default=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_remote_control_script'

    def __unicode__(self):
        return str(self.id)


class Remote_Control_Copy(models.Model):
    desc = models.CharField(max_length=128, blank=False, null=False, unique=True)
    src = models.CharField(max_length=256, blank=False, null=False)
    dest = models.CharField(max_length=256, blank=True, null=True, default='')
    authority = models.CharField(max_length=8, blank=False, null=False, default='755')
    src_url = models.CharField(max_length=256, blank=True, null=True)
    src_username = models.CharField(max_length=64, blank=True, null=True)
    src_password = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_remote_control_copy'

    def __unicode__(self):
        return str(self.id)


class Business_Tree(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    data = models.TextField(blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_business_tree'

    def __unicode__(self):
        return str(self.id)


class Asset_Tag(models.Model):
    name = models.CharField(max_length=1024, blank=False, null=False)
    asset = models.ManyToManyField(Asset, through='Asset_Tag_Data', blank=True, null=True)
    ontree = models.BooleanField(default=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_tag'

    def __unicode__(self):
        return self.name


class Asset_Tag_Data(models.Model):
    asset_tag = models.ForeignKey(Asset_Tag, related_name='Asset_Tag_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    asset = models.ForeignKey(Asset, related_name='Asset_Tag_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_asset_tag_data'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Work_Result(models.Model):
    data = models.TextField(blank=True, null=True)
    success = models.BooleanField(default=True)
    jobs = models.TextField(blank=False, null=False)
    modtime = models.DateTimeField(help_text=u'最后修改时间', blank=False, null=False)
    type = models.CharField(max_length=8, blank=False, null=False, default='online')

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_work_result'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Work(models.Model):
    name_cn = models.CharField(max_length=1024, blank=True, null=True)
    name_en = models.CharField(max_length=1024, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    jobs = models.TextField(blank=False, null=False)
    test_tag = models.ForeignKey(Asset_Tag, related_name='Configure_Manage_Work', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField(Asset_Tag, through='Configure_Manage_Work_Tag_Data', blank=False, null=False)
    timeout = models.IntegerField(help_text=u'超时时间,单位分钟', blank=False, null=False, default=1)
    sync = models.BooleanField(default=True)
    status = models.IntegerField(help_text=u'当前状态,0未进行，1测试中，2测试成功，3测试失败，4执行中，5执行成功，6执行失败， 7忽略测试失败， 8忽略执行失败', blank=False, null=False, default=0)
    result = models.ManyToManyField(Configure_Manage_Work_Result, through='Configure_Manage_Work_Result_Data', blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_work'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Work_Tag_Data(models.Model):
    work = models.ForeignKey(Configure_Manage_Work, related_name='Configure_Manage_Work_Tag_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    asset_tag = models.ForeignKey(Asset_Tag, related_name='Configure_Manage_Work_Tag_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    begin = models.BooleanField(default=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_work_tag_data'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Work_Result_Data(models.Model):
    work = models.ForeignKey(Configure_Manage_Work, related_name='Configure_Manage_Work_Result_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    result = models.ForeignKey(Configure_Manage_Work_Result, related_name='Configure_Manage_Work_Result_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    asset = models.ForeignKey(Asset, related_name='Configure_Manage_Work_Result_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_work_result_data'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Task(models.Model):
    name_cn = models.CharField(max_length=1024, blank=True, null=True)
    name_en = models.CharField(max_length=1024, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    time_auto_exec = models.DateTimeField(blank=True, null=True)
    work = models.ManyToManyField(Configure_Manage_Work, through='Configure_Manage_Task_Data', blank=False, null=False)
    status = models.IntegerField(help_text=u'当前状态,0未进行，1测试中，2测试成功，3测试失败，4执行中，5执行成功，6执行失败', blank=False, null=False, default=0)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_task'

    def __unicode__(self):
        return str(self.id)


class Configure_Manage_Task_Data(models.Model):
    work = models.ForeignKey(Configure_Manage_Work, related_name='Configure_Manage_Task_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    task = models.ForeignKey(Configure_Manage_Task, related_name='Configure_Manage_Task_Data', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    check_true = models.BooleanField(default=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_configure_manage_task_data'

    def __unicode__(self):
        return str(self.id)


class Authority_Url(models.Model):
    url = models.CharField(max_length=128, blank=False, null=False, db_index=True)
    user = models.ForeignKey(User, related_name='Authority_Url', to_field='id', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_authority_url'

    def __unicode__(self):
        return str(self.id)


class Bussiness(models.Model):
    name_cn = models.CharField(max_length=1024, blank=True, null=True)
    name_en = models.CharField(max_length=1024, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name='Bussiness', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    person = models.ManyToManyField(User, through='Authority_Bussiness', blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_bussiness'

    def __unicode__(self):
        return str(self.id)


class Authority_Bussiness(models.Model):
    bussiness = models.ForeignKey(Bussiness, related_name='Authority_Bussiness', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, related_name='Authority_Bussiness', to_field='id', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_authority_bussiness'

    def __unicode__(self):
        return str(self.id)


class Bussiness_Btn(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    bussiness = models.ForeignKey(Bussiness, related_name='Bussiness_Btns', to_field='id', on_delete=models.CASCADE, blank=False, null=False)
    work = models.ForeignKey(Configure_Manage_Work, related_name='Bussiness_Btns', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Configure_Manage_Task, related_name='Bussiness_Btns', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        app_label = 'APP_web'
        db_table = 'tb_bussiness_btn'

    def __unicode__(self):
        return str(self.id)