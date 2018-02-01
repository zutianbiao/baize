#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统自动工作插件中的作业管理插件


###################################################################################################
import sys
import hashlib
import base64
import os
import time
import json
from gevent import monkey
monkey.patch_all()
import gevent
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import baize.settings as C
import logging
import API.API_agent.constant as A_C
from API.API_agent.plugins.base import Task_Reporter, Task_Creater, Task_Processor, request
from API.API_agent.config_items import Config
from API.API_agent.remote_control import remote_control_shell, remote_control_script, remote_control_copy
from APP.APP_agent.models import Configure_Manage_Work


def do_work(work):
    result = []
    success = True
    for j in work['jobs']:
        if j['type'] == 'command':
            json_module_args = {'command': j['command']}
            re = remote_control_shell(json_module_args=json_module_args, int_timeout=work['timeout']*60)
            result.append(re)
            if not j['ignore_error'] and not re['success']:
                success = False
                break
        elif j['type'] == 'script':
            json_module_args = {
                "script": j['script'],
                "args": j['args'],
            }
            re = remote_control_script(json_module_args=json_module_args, int_timeout=work['timeout']*60)
            result.append(re)
            if not j['ignore_error'] and not re['success']:
                success = False
                break
        elif j['type'] == 'copy':
            json_module_args = {
                "src": j['src'],
                "dest": j['dest'],
                "mode": j['authority'],
            }
            re = remote_control_copy(json_module_args=json_module_args, int_timeout=work['timeout']*60)
            result.append(re)
            if not j['ignore_error'] and not re['success']:
                success = False
                break
            if re['success'] and j['check_change']:
                if not re['msg']['changed']:
                    success = False
                    break
    work['result'] = result
    work['success'] = success
    if success:
        msg = u"作业%s执行成功" % work['name_cn']
        logger = logging.getLogger('log_file')
        logger.info(msg)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.info(msg)
    else:
        msg = u"作业%s执行失败" % work['name_cn']
        logger = logging.getLogger('log_file')
        logger.error(msg)
        if C.LOG_SCREEN == 'ON':
            logger = logging.getLogger('log_screen')
            logger.error(msg)
    C_agent = Config()
    json_report = {
        "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
        "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
        "data": []
    }
    json_report['data'].append(work)
    return json_report


class Task_Work_Manage_Creater(Task_Creater):
    """ 作业管理任务生成器 """

    def _get_tasks(self):
        C_agent = Config()
        data = {
            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None)
        }
        try:
            if data['hostname'] and data['sn']:
                try:
                    response_data = request(A_C.URL_WORK_MANAGE_TASK, data=data, timeout=300)
                except Exception, e:
                    msg = u"抓取任务超时"
                    logger = logging.getLogger('log_file')
                    logger.error(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.error(msg)
                    return False, {}
                if not isinstance(response_data, dict):
                    try:
                        response_data = eval(response_data)
                    except Exception, e:
                        response_data = json.loads(str(response_data))
                if response_data['success']:
                    if not isinstance(response_data['data'], list):
                        response_data['data'] = json.loads(response_data['data'])
                    list_work = response_data['data']
                    for work in list_work:
                        jobs = work['jobs']
                        msg = u"抓取到作业%s" % work['name_cn']
                        logger = logging.getLogger('log_file')
                        logger.info(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.info(msg)
                        for json_module_args in jobs:
                            if json_module_args['type'] == 'script':
                                if isinstance(json_module_args['script'], unicode):
                                    json_module_args['script'] = json_module_args['script'].encode('utf8')

                                if isinstance(json_module_args['script'], list):
                                    string_script_name = os.path.join(os.path.dirname(__file__), "../../../static/upload/Script_auto_"+json_module_args['md5'])
                                    dir_script_name = os.path.dirname(string_script_name)
                                    if not os.path.exists(dir_script_name):
                                        os.makedirs(dir_script_name)
                                    obj_fp = open(string_script_name, 'w')
                                    for _line in json_module_args['script']:
                                        obj_fp.write(_line.encode('utf8'))
                                    obj_fp.close()
                                    if hashlib.md5(open(string_script_name, 'rb').read()).hexdigest() == json_module_args['md5']:
                                        json_module_args['script'] = string_script_name
                                    else:
                                        msg = u"%s文件MD5不一致" % json_module_args['dest']
                                        logger = logging.getLogger('log_file')
                                        logger.error(msg)
                                        if C.LOG_SCREEN == 'ON':
                                            logger = logging.getLogger('log_screen')
                                            logger.error(msg)
                                        return False, {}
                            elif json_module_args['type'] == 'copy':
                                if isinstance(json_module_args['src'], unicode):
                                    json_module_args['src'] = json_module_args['src'].encode('utf8')

                                if isinstance(json_module_args['src'], list):
                                    string_script_name = os.path.join(os.path.dirname(__file__), "../../../files/scripts/upload/Copy_auto_"+json_module_args['md5'])
                                    obj_fp = open(string_script_name, 'w')
                                    for line in json_module_args['src']:
                                        obj_fp.write(line.encode('utf8'))
                                    obj_fp.close()
                                    if hashlib.md5(open(string_script_name, 'rb').read()).hexdigest() == json_module_args['md5']:
                                        json_module_args['src'] = string_script_name
                                    else:
                                        msg = u"%s文件MD5不一致" % json_module_args['dest']
                                        logger = logging.getLogger('log_file')
                                        logger.error(msg)
                                        if C.LOG_SCREEN == 'ON':
                                            logger = logging.getLogger('log_screen')
                                            logger.error(msg)
                                        return False, {}
                                else:
                                    json_module_args['src'] = base64.b64decode(json_module_args['src'])
                                    string_script_name = os.path.join(os.path.dirname(__file__), "../../../files/scripts/upload/Copy_auto_"+json_module_args['md5'])
                                    obj_fp = open(string_script_name, 'wb')
                                    obj_fp.write(json_module_args['src'])
                                    obj_fp.close()
                                    if hashlib.md5(open(string_script_name, 'rb').read()).hexdigest() == json_module_args['md5']:
                                        json_module_args['src'] = string_script_name
                                    else:
                                        msg = u"%s文件MD5不一致" % json_module_args['dest']
                                        logger = logging.getLogger('log_file')
                                        logger.error(msg)
                                        if C.LOG_SCREEN == 'ON':
                                            logger = logging.getLogger('log_screen')
                                            logger.error(msg)
                                        return False, {}
                        if isinstance(jobs, list):
                            jobs = json.dumps(jobs)
                        try:
                            _configure_manage_work = Configure_Manage_Work.objects.get(jobs=jobs, name_cn=work['name_cn'], name_en=work['name_en'], sync=work['sync'], timeout=work['timeout'], desc=work['desc'], type=work['type'])
                            if _configure_manage_work.status == 1 or _configure_manage_work.status == 4:
                                msg = u"作业%s正在执行中" % work['name_cn']
                                logger = logging.getLogger('log_file')
                                logger.info(msg)
                                if C.LOG_SCREEN == 'ON':
                                    logger = logging.getLogger('log_screen')
                                    logger.info(msg)
                                list_work.remove(work)
                            elif _configure_manage_work.status != 0:
                                msg = u"新增作业%s发现已经有结果" % work['name_cn']
                                logger = logging.getLogger('log_file')
                                logger.info(msg)
                                if C.LOG_SCREEN == 'ON':
                                    logger = logging.getLogger('log_screen')
                                    logger.info(msg)
                            else:
                                msg = u"新增作业%s发现已存在" % work['name_cn']
                                logger = logging.getLogger('log_file')
                                logger.info(msg)
                                if C.LOG_SCREEN == 'ON':
                                    logger = logging.getLogger('log_screen')
                                    logger.info(msg)
                        except Exception, e:
                            msg = u"新增作业%s" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.info(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.info(msg)
                            _configure_manage_work = Configure_Manage_Work(jobs=jobs, name_cn=work['name_cn'], name_en=work['name_en'], sync=work['sync'], timeout=work['timeout'], desc=work['desc'], type=work['type'], status=0)
                            _configure_manage_work.save()
                    response_data['data'] = list_work
                    return True, response_data
                else:
                    msg = u"作业抓取失败"
                    logger = logging.getLogger('log_file')
                    logger.error(msg)
                    if C.LOG_SCREEN == 'ON':
                        logger = logging.getLogger('log_screen')
                        logger.error(msg)
                    return False, {}
            else:
                return False, {}
        except Exception, e:
            return False, {}


class Task_Work_Manage_Processor_Test(Task_Processor):
    """ 测试作业管理任务处理 """

    def _loop(self):
        while self.on:
            if not self.inqueue.empty():
                task = self.inqueue.get()
                if not isinstance(task, dict):
                    task = json.loads(task)
                work = task
                jobs = work['jobs']
                if isinstance(jobs, list):
                    jobs = json.dumps(jobs)
                if task['type'] == 'test':
                    try:
                        _configure_manage_work = Configure_Manage_Work.objects.get(jobs=jobs, name_cn=work['name_cn'], name_en=work['name_en'], sync=work['sync'], timeout=work['timeout'], desc=work['desc'], type=work['type'])
                    except Exception, e:
                        msg = u"作业%s数据丢失" % work['name_cn']
                        logger = logging.getLogger('log_file')
                        logger.error(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.error(msg)
                        continue
                    if _configure_manage_work.status == 0:
                        try:
                            _configure_manage_work2 = Configure_Manage_Work.objects.filter(sync=False, type='test', status=1)
                            if len(_configure_manage_work2) >= 1:
                                msg = u"作业%s不允许并行，其他任务等待" % _configure_manage_work2[0].name_cn
                                logger = logging.getLogger('log_file')
                                logger.info(msg)
                                if C.LOG_SCREEN == 'ON':
                                    logger = logging.getLogger('log_screen')
                                    logger.info(msg)
                                continue
                            else:
                                _configure_manage_work.status = 1
                                _configure_manage_work.save()
                                task = do_work(task)
                                self.outqueue.put(task)
                        except Exception, e:
                            msg = e
                            logger = logging.getLogger('log_file')
                            logger.warning(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.warning(msg)
                            _configure_manage_work.status = 1
                            _configure_manage_work.save()
                            task = do_work(task)
                            self.outqueue.put(task)
                    elif _configure_manage_work.status == 2:
                        result = _configure_manage_work.result
                        success = True
                        work['result'] = result
                        work['success'] = success
                        if success:
                            msg = u"作业%s已存在并且执行成功" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.info(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.info(msg)
                        else:
                            msg = u"作业%s已存在并且执行失败" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)
                        C_agent = Config()
                        json_report = {
                            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                            "data": []
                        }
                        json_report['data'].append(work)
                        self.outqueue.put(json_report)
                    elif _configure_manage_work.status == 3:
                        result = _configure_manage_work.result
                        success = False
                        work['result'] = result
                        work['success'] = success
                        if success:
                            msg = u"作业%s已存在并且执行成功" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.info(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.info(msg)
                        else:
                            msg = u"作业%s已存在并且执行失败" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)
                        C_agent = Config()
                        json_report = {
                            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                            "data": []
                        }
                        json_report['data'].append(work)
                        self.outqueue.put(json_report)
                    else:
                        continue
            else:
                gevent.sleep(1)


class Task_Work_Manage_Processor_Online(Task_Processor):
    """ 在线作业管理任务处理 """

    def _loop(self):
        while self.on:
            if not self.inqueue.empty():
                task = self.inqueue.get()
                if not isinstance(task, dict):
                    task = json.loads(task)
                work = task
                jobs = work['jobs']
                if isinstance(jobs, list):
                    jobs = json.dumps(jobs)
                if task['type'] == 'online':
                    try:
                        _configure_manage_work = Configure_Manage_Work.objects.get(jobs=jobs, name_cn=work['name_cn'], name_en=work['name_en'], sync=work['sync'], timeout=work['timeout'], desc=work['desc'], type=work['type'])
                    except Exception, e:
                        msg = u"作业%s数据丢失" % work['name_cn']
                        logger = logging.getLogger('log_file')
                        logger.error(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.error(msg)
                        continue
                    if _configure_manage_work.status < 4:
                        try:
                            _configure_manage_work2 = Configure_Manage_Work.objects.filter(sync=False, type='online', status=4)
                            if len(_configure_manage_work2) >= 1:
                                msg = u"作业%s不允许并行，其他任务等待" % _configure_manage_work2[0].name_cn
                                logger = logging.getLogger('log_file')
                                logger.info(msg)
                                if C.LOG_SCREEN == 'ON':
                                    logger = logging.getLogger('log_screen')
                                    logger.info(msg)
                                continue
                            else:
                                _configure_manage_work.status = 4
                                _configure_manage_work.save()
                                task = do_work(task)
                                self.outqueue.put(task)
                        except Exception, e:
                            _configure_manage_work.status = 4
                            _configure_manage_work.save()
                            task = do_work(task)
                            self.outqueue.put(task)
                    elif _configure_manage_work.status == 5:
                        result = _configure_manage_work.result
                        success = True
                        work['result'] = result
                        work['success'] = success
                        if success:
                            msg = u"作业%s已存在并且执行成功" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.info(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.info(msg)
                        else:
                            msg = u"作业%s已存在并且执行失败" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)
                        C_agent = Config()
                        json_report = {
                            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                            "data": []
                        }
                        json_report['data'].append(work)
                        self.outqueue.put(json_report)
                    elif _configure_manage_work.status == 6:
                        result = _configure_manage_work.result
                        success = False
                        work['result'] = result
                        work['success'] = success
                        if success:
                            msg = u"作业%s已存在并且执行成功" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.info(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.info(msg)
                        else:
                            msg = u"作业%s已存在并且执行失败" % work['name_cn']
                            logger = logging.getLogger('log_file')
                            logger.error(msg)
                            if C.LOG_SCREEN == 'ON':
                                logger = logging.getLogger('log_screen')
                                logger.error(msg)
                        C_agent = Config()
                        json_report = {
                            "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                            "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                            "data": []
                        }
                        json_report['data'].append(work)
                        self.outqueue.put(json_report)
                    else:
                        continue
            else:
                gevent.sleep(1)


class Task_Work_Manage_Reporter(Task_Reporter):
    """ 作业管理任务上报器 """

    def _loop(self):
        while self.on:
            if not self.queue.empty():
                data = self.queue.get()
                list_work = data['data']
                for work in list_work:
                    jobs = work['jobs']
                    name_cn = work['name_cn']
                    if isinstance(jobs, list):
                        jobs = json.dumps(jobs)
                    try:
                        _configure_manage_work = Configure_Manage_Work.objects.get(jobs=jobs, name_cn=work['name_cn'], name_en=work['name_en'], sync=work['sync'], timeout=work['timeout'], desc=work['desc'], type=work['type'])
                    except Exception, e:
                        continue
                    if work['type'] == 'test':
                        if work['success']:
                            _configure_manage_work.status = 2
                        else:
                            _configure_manage_work.status = 3
                    else:
                        if work['success']:
                            _configure_manage_work.status = 5
                        else:
                            _configure_manage_work.status = 6
                    if isinstance(work['result'], list):
                        work['result'] = json.dumps(work['result'])
                    _configure_manage_work.result = work['result']
                    _configure_manage_work.save()
                data['time'] = time.time()
                C_agent = Config()
                json_report = {
                    "hostname": C_agent.item(item_name='HOSTNAME', group_name='ASSET', default=None),
                    "sn": C_agent.item(item_name='SN', group_name='ASSET', default=None),
                    "data": []
                }
                json_report['data'].append(data)
                if json_report['hostname'] and json_report['sn']:
                    report_re = self._report_tasks(data=json_report, reciver='work_manage')
                    if report_re['success']:
                        msg = u"作业%s结果上报成功" % name_cn
                        logger = logging.getLogger('log_file')
                        logger.info(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.info(msg)
                    else:
                        msg = u"作业%s结果上报失败" % name_cn
                        logger = logging.getLogger('log_file')
                        logger.error(msg)
                        if C.LOG_SCREEN == 'ON':
                            logger = logging.getLogger('log_screen')
                            logger.error(msg)
                json_report['data'] = []
            else:
                gevent.sleep(1)


class Work_Manage_Task_Test(object):
    """ 作业管理任务的抽象类 """
    def __init__(self, worknum=A_C.PROCESS_NUM):
        self.reporter = Task_Work_Manage_Reporter()
        self.creater = Task_Work_Manage_Creater()
        self.workers = []
        self.on = False
        for i in xrange(worknum):
            self.workers.append(Task_Work_Manage_Processor_Test(self.creater.queue, self.reporter.queue))

    def start(self):
        self.on = True
        self.creater.start()
        for worker in self.workers:
            worker.start()
        self.reporter.start()
        self._loop()

    def stop(self):
        self.on = False
        self.creater.stop()
        for worker in self.workers:
            worker.stop()
        self.reporter.stop()

    def _loop(self):
        cur_time = time.time() - A_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < A_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t


class Work_Manage_Task_Online(object):
    """ 作业管理任务的抽象类 """
    def __init__(self, worknum=A_C.PROCESS_NUM):
        self.reporter = Task_Work_Manage_Reporter()
        self.creater = Task_Work_Manage_Creater()
        self.workers = []
        self.on = False
        for i in xrange(worknum):
            self.workers.append(Task_Work_Manage_Processor_Online(self.creater.queue, self.reporter.queue))

    def start(self):
        self.on = True
        self.creater.start()
        for worker in self.workers:
            worker.start()
        self.reporter.start()
        self._loop()

    def stop(self):
        self.on = False
        self.creater.stop()
        for worker in self.workers:
            worker.stop()
        self.reporter.stop()

    def _loop(self):
        cur_time = time.time() - A_C.INTERVAL_CHECK
        while self.on:
            t = time.time()
            if t - cur_time < A_C.INTERVAL_CHECK:
                gevent.sleep(1)
                continue
            cur_time = t

if __name__ == '__main__':
    work_manage_task = Work_Manage_Task_Test()
    work_manage_task.start()
