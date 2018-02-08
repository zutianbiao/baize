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
import datetime
from API.API_web.plugins.base import Worker
from APP.APP_web.models import Alarm_Msg
from baize.settings import INTERVAL_WORKER
from django.core.mail import send_mail
from API.API_web.smss_send import send
from django.utils import timezone


class Alarm_Msg_Sender(Worker):
    """ 报警处理器"""

    def do(self):

        now = timezone.now()
        _mins = datetime.timedelta(minutes=5)
        time_from = now - _mins
        alarm_msg = Alarm_Msg.objects.filter(modtime__gte=time_from, status=0)
        for a_m in alarm_msg:
            a_m.status = 1
            a_m.save()
        if len(alarm_msg) > 100:
            self.interval = INTERVAL_WORKER
        else:
            self.interval = 5
        for a_m in alarm_msg:
            send_tag = True
            if a_m.alarm.switch:
                list_email = list()
                list_phone_number = list()
                for person in a_m.alarm.person.all():
                    list_phone_number.append(str(person.phone))
                    list_email.append(person.email)
                phone_number = ','.join(list_phone_number)
                if a_m.alarm.method in [0, 2]:
                    if phone_number:
                        tag = send(phone_number, u"%s【白泽报警中心】" % a_m.msg)
                        if tag != True:
                            send_tag = False
                            msg = u"【报警短信发送失败】消息id: %d" % a_m.id
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)

                if a_m.alarm.method in [1, 2]:
                    if list_email:
                        try:
                            send_mail(u'【白泽】监控报警', u"%s【白泽报警中心】" % a_m.msg, C.EMAIL_HOST_USER, list_email, fail_silently=False)
                        except Exception, e:
                            send_tag = False
                            msg = u"【报警邮件发送失败】消息id: %d" % a_m.id
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)
            if send_tag:
                a_m.status = 2
            else:
                a_m.status = 3
            a_m.save()


if __name__ == '__main__':
    alarm_msg_sender = Alarm_Msg_Sender()
    alarm_msg_sender.start()
