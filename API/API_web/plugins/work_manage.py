#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件中的作业管理插件


###################################################################################################
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import baize.settings as C
import logging
from API.API_web.plugins.base import Worker
from APP.APP_web.views import work_status_refresh
from APP.APP_web.models import Configure_Manage_Work, Configure_Manage_Work_Result_Data
from baize.settings import INTERVAL_WORKER


def gray_update(work):
    list_tag_data = []
    tag_data = work.Configure_Manage_Work_Tag_Data.all()
    for t_d in tag_data:
        list_tag_data.append(t_d)
    try:
        work_tag_data = work.Configure_Manage_Work_Tag_Data.get(begin=True)
    except Exception, e:
        if list_tag_data:
            work_tag_data = list_tag_data[0]
            work_tag_data.begin = True
            work_tag_data.save()

    result_summary = {
        "success": {},
        "failed": {},
        "unknown": {}
    }
    _asset = work_tag_data.asset_tag.asset.all()
    for a in _asset:
        result_summary['unknown'][a.id] = {
            "hostname": a.name,
            "sn": a.sn,
        }
        try:
            _work_result_data = Configure_Manage_Work_Result_Data.objects.filter(work=work, asset=a)
            for wrd in _work_result_data:
                if wrd.result.type == 'online':
                    if wrd.result.success:
                        result_summary['success'][a.id] = {
                            "hostname": a.name,
                            "sn": a.sn,
                            "result": wrd.result.data,
                        }
                        del result_summary['unknown'][a.id]
                    else:
                        result_summary['failed'][a.id] = {
                            "hostname": a.name,
                            "sn": a.sn,
                            "result": wrd.result.data,
                        }
                        del result_summary['unknown'][a.id]
        except Exception, e:
            pass

    num_asset_unknown = len(result_summary['unknown'])
    num_asset_success = len(result_summary['success'])
    num_asset_failed = len(result_summary['failed'])
    if num_asset_unknown == 0 and num_asset_failed == 0:
        msg = u"作业:%s,标签:%s【升级完成】" % (work.name_cn, work_tag_data.asset_tag.name)
        logger = logging.getLogger('log_file')
        logger.info(msg)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.info(msg)
        work_tag_data.begin = False
        work_tag_data.save()
        list_tag_data.remove(work_tag_data)
        if list_tag_data:
            work_tag_data = list_tag_data[0]
            work_tag_data.begin = True
            work_tag_data.save()


class Work_Manage_Gray_Upgrade(Worker):
    """ 作业管理灰度升级worker"""

    def do(self):

        list_work = Configure_Manage_Work.objects.filter(status=4)
        for work in list_work:
            gray_update(work)

        work_status = [1, 4]
        list_work = Configure_Manage_Work.objects.filter(status__in=work_status)
        for work in list_work:
            work_status_refresh(work.id)
        if len(list_work) > 100:
            self.interval = INTERVAL_WORKER
        else:
            self.interval = 5

if __name__ == '__main__':
    work_manage_gray_update = Work_Manage_Gray_Upgrade()
    work_manage_gray_update.start()