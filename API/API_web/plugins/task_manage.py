#!/usr/local/baize/env/bin/python
# coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件中的作业管理插件


###################################################################################################
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import datetime
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from API.API_web.plugins.base import Worker
from APP.APP_web.models import Configure_Manage_Task
# from API.API_web.smss_send import send
from baize.settings import INTERVAL_WORKER
###################################################################################################
# 报警到的手机号(多个手机号使用逗号','分隔)
STR_PHONE_LIST = '18611642164'
###################################################################################################


def gray_update_task(task):
    """ 灰度升级任务 """
    time_now = time.time()
    if task.status == 2:
        time_auto_exec = time.mktime(task.time_auto_exec.timetuple())
        if time_auto_exec > 0 and time_auto_exec < time_now - 8 * 60 * 60:
            task.status = 4
            task.time_auto_exec = datetime.datetime.fromtimestamp(time.mktime(time.strptime('1970-1-1 08:00', "%Y-%m-%d %H:%M")))
            task.save()

    works = task.work.all()
    if task.status == 4:
        for w in works:
            if w.status == 2:
                w.status = 4
                w.save()
                break
            elif w.status == 5 or w.status == 7 or w.status == 8:
                continue
            else:
                break


def task_status_refresh(task):
    """ 更新任务状态 """
    works = task.work.all()
    list_status = [0, 0, 0, 0, 0, 0, 0]
    for w in works:
        if w.status == 7:
            list_status[3] += 1
        elif w.status == 8:
            list_status[6] += 1
        else:
            list_status[w.status] += 1

    if list_status[0:2] == [0, 0] and list_status[3:] == [0, 0, 0, 0] and list_status[2] != 0:
        task.status = 2
    elif list_status[0:5] == [0, 0, 0, 0, 0] and list_status[6] == 0 and list_status[5] != 0:
        task.status = 5
    elif list_status[1] != 0:
        task.status = 1
    elif list_status[3] != 0:
        task.status = 3
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = "【%s】【白泽系统】任务:%s测试失败" % (time_now, task.name_cn)
        # send(phone=STR_PHONE_LIST, msg=msg)
    elif list_status[4] != 0:
        task.status = 4
    elif list_status[6] != 0:
        task.status = 6
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = "【%s】【白泽系统】任务:%s执行失败" % (time_now, task.name_cn)
        # send(phone=STR_PHONE_LIST, msg=msg)
    elif list_status[0] != 0:
        task.status = 0

    task.save()


class Task_Manage_Gray_Upgrade(Worker):
    """ 任务管理灰度升级worker"""

    def do(self):

        list_task = Configure_Manage_Task.objects.filter(status__in=[2, 4])
        for task in list_task:
            gray_update_task(task)

        task_status = [1, 4]
        list_task = Configure_Manage_Task.objects.filter(status__in=task_status)
        for task in list_task:
            task_status_refresh(task)
        if len(list_task) > 100:
            self.interval = INTERVAL_WORKER
        else:
            self.interval = 5

if __name__ == '__main__':
    task_manage_gray_update = Task_Manage_Gray_Upgrade()
    task_manage_gray_update.start()
