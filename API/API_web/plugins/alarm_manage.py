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
import time
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


def alert_local(a_m, msg2):
    send_tag = True
    list_email = list()
    list_phone_number = list()
    for person in a_m.template.alarm.person.all():
        list_phone_number.append(str(person.phone))
        list_email.append(person.email)
    phone_number = ','.join(list_phone_number)
    if a_m.template.alarm.method in [0, 2]:
        if phone_number:
            tag = send(phone_number, msg2)
            if tag != True:
                send_tag = False
                msg = u"【报警短信发送失败】消息id: %d" % a_m.id
                logger = logging.getLogger('log_file')
                logger.error(msg)
                if C.LOG_SCREEN == 'ON':
                    logger = logging.getLogger('log_screen')
                    logger.error(msg)

    if a_m.template.alarm.method in [1, 2]:
        if list_email:
            try:
                send_mail(u'【白泽】监控报警', msg2, C.EMAIL_HOST_USER, list_email, fail_silently=False)
            except Exception, e:
                send_tag = False
                msg = u"【报警邮件发送失败】消息id: %d" % a_m.id
                logger = logging.getLogger('log_file')
                logger.error(msg)
                if C.LOG_SCREEN == 'ON':
                    logger = logging.getLogger('log_screen')
                    logger.error(msg)
    return send_tag


class Alarm_Msg_Sender(Worker):
    """ 报警处理器"""

    def do(self):

        now = timezone.now()
        _mins = datetime.timedelta(minutes=5)
        time_from = now - _mins
        alarm_msg = Alarm_Msg.objects.filter(modtime__gte=time_from, status=0)
        dict_combine = dict()
        for a_m in alarm_msg:
            if a_m.template.alarm.switch:
                try:
                    a_m.template.Alarm_Msg_Ignore.get(key_string=a_m.key_string)
                    a_m.status = 7
                    a_m.save()
                except Exception, e:
                    if a_m.template.combine:
                        if a_m.key_string not in dict_combine:
                            _mins = datetime.timedelta(minutes=a_m.template.combine_period)
                            time_from = now - _mins
                            alarm_msg2 = Alarm_Msg.objects.filter(modtime__gte=time_from, key_string=a_m.key_string)
                            dict_combine[a_m.key_string] = list()
                            for a_m2 in alarm_msg2:
                                if a_m2.status <= 1:
                                    a_m2.status = 10
                                    a_m2.save()
                                    dict_combine[a_m.key_string].append(int(a_m2.id))
                    else:
                        a_m.status = 1
                        a_m.save()
            else:
                a_m.status = 7
                a_m.save()

        if len(alarm_msg) > 100:
            self.interval = INTERVAL_WORKER
        else:
            self.interval = 5
        for a_m in alarm_msg:
            if a_m.status == 1:
                msg2 = u"%s【白泽报警中心】" % a_m.msg
                send_tag = alert_local(a_m, msg2)
                if send_tag:
                    a_m.status = 2
                else:
                    a_m.status = 3
                a_m.save()
        for key, value in dict_combine.items():
            value.sort()
            id = value[-1]
            a_m = Alarm_Msg.objects.get(id=id)
            a_m_timestamp = time.mktime(a_m.modtime.timetuple())
            _mins = datetime.timedelta(minutes=a_m.template.combine_period * 2)
            time_from = now - _mins
            alarm_msg2 = Alarm_Msg.objects.filter(modtime__gte=time_from, key_string=a_m.key_string, status__in=[2, 3, 5, 6]).exclude(id__in=value).order_by('-modtime')
            send_tag2 = False
            if len(alarm_msg2) <= 0:
                send_tag2 = True
            else:
                a_m_timestamp2 = time.mktime(alarm_msg2[0].modtime.timetuple())
                if a_m_timestamp > a_m_timestamp2 + a_m.template.combine_period * 60:
                    send_tag2 = True
            if send_tag2:
                _mins = datetime.timedelta(minutes=a_m.template.combine_period * 2)
                time_from = now - _mins
                alarm_msg4 = Alarm_Msg.objects.filter(modtime__gte=time_from, key_string=a_m.key_string)
                msg2 = u"%s,%d分钟内同类报警共计%d条【白泽报警中心】" % (a_m.msg, a_m.template.combine_period, len(alarm_msg4))
                send_tag = alert_local(a_m, msg2)
                if send_tag:
                    alarm_msg2 = Alarm_Msg.objects.filter(id__in=value).exclude(id=id)
                    for a_m2 in alarm_msg2:
                        a_m2.status = 8
                        a_m2.save()
                    a_m.status = 2
                else:
                    alarm_msg2 = Alarm_Msg.objects.filter(id__in=value).exclude(id=id)
                    for a_m2 in alarm_msg2:
                        a_m2.status = 9
                        a_m2.save()
                    a_m.status = 3
                a_m.save()
            else:
                alarm_msg3 = Alarm_Msg.objects.filter(id__in=value)
                for a_m3 in alarm_msg3:
                    if alarm_msg2[0].status in [2, 5]:
                        a_m3.status = 8
                    elif alarm_msg2[0].status in [3, 6]:
                        a_m3.status = 9
                    a_m3.save()


if __name__ == '__main__':
    alarm_msg_sender = Alarm_Msg_Sender()
    alarm_msg_sender.start()
