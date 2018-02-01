#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Agent的远程控制API


###################################################################################################
import base64
import ansible.runner
import time
import os
import ansible.utils
import ansible.callbacks
import ansible.playbook
import ansible.constants as CS


def remote_control_shell(json_module_args={'command': 'hostname'}, int_timeout=30, int_background=0):
    """
    远程shell
    参数:
        json_module_args        传递模块参数,Demo: {'command': 'hostname'}
        int_timeout             模块运行超时
        int_background          模块是否后台运行
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    obj_runner = ansible.runner.Runner(
        host_list=['127.0.0.1'],
        run_hosts=['127.0.0.1'],
        transport='local',
        module_name='shell',
        timeout=int_timeout,
        background=int_background,
        module_args=json_module_args['command']
    )
    try:
        json_data = obj_runner.run()
        _stdout = json_data['contacted']['127.0.0.1']
    except Exception, e:
        return {"success": False, "msg": e}
    return {"success": True, "msg": _stdout}


def remote_control_script(json_module_args, int_timeout=30, int_background=0):
    """
    远程shell
    参数:
        json_module_args        传递模块参数,Demo: {'script': '脚本内容列表或者agent本地脚本路径', "args": ""}
        int_timeout             模块运行超时
        int_background          模块是否后台运行
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    if 'args' in json_module_args:
        if isinstance(json_module_args['args'], unicode):
            json_module_args['args'] = json_module_args['args'].encode('utf8')
        args = json_module_args['args']
    else:
        args = ''

    if isinstance(json_module_args['script'], unicode):
        json_module_args['script'] = json_module_args['script'].encode('utf8')

    if isinstance(json_module_args['script'], list):
        string_script_name = os.path.join(os.path.dirname(__file__), "../../static/upload/Script_auto_%.6f" % time.time())
        dir_script_name = os.path.dirname(string_script_name)
        if not os.path.exists(dir_script_name):
                os.makedirs(dir_script_name)
        obj_fp = open(string_script_name, 'w')
        for _line in json_module_args['script']:
            obj_fp.write(_line.encode('utf8'))
        obj_fp.close()
        json_module_args['script'] = string_script_name

    if isinstance(json_module_args['script'], str):
        try:
            os.chmod(json_module_args['script'], 0755)
        except Exception, e:
            return {"success": False, "msg": e}
        obj_runner = ansible.runner.Runner(
            host_list=['127.0.0.1'],
            run_hosts=['127.0.0.1'],
            transport='local',
            module_name='shell',
            timeout=int_timeout,
            background=int_background,
            module_args=json_module_args['script'] + ' ' + args
        )
        try:
            json_data = obj_runner.run()
            _stdout = json_data['contacted']['127.0.0.1']
        except Exception, e:
            return {"success": False, "msg": e}
        return {"success": True, "msg": _stdout}

    return {"success": False, "msg": u"脚本不合法"}


def remote_control_copy(json_module_args, int_timeout=30, int_background=0):
    """
    远程shell
    参数:
        json_module_args        传递模块参数,Demo: {'src': '脚本内容列表或者agent本地脚本路径', 'dest': '脚本存放的目标路径', 'mode': '目标文件的权限默认755'}
        int_timeout             模块运行超时
        int_background          模块是否后台运行
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    mode = int(json_module_args.get('mode', '755'))

    if isinstance(json_module_args['src'], unicode):
        json_module_args['src'] = json_module_args['src'].encode('utf8')

    if isinstance(json_module_args['src'], list):
        string_script_name = os.path.join(os.path.dirname(__file__), "../../files/scripts/upload/copy_auto_%.6f" % time.time())
        obj_fp = open(string_script_name, 'w')
        for line in json_module_args['src']:
            obj_fp.write(line.encode('utf8'))
        obj_fp.close()
        json_module_args['src'] = string_script_name
    else:
        try:
            json_module_args['src'] = base64.b64decode(json_module_args['src'])
            string_script_name = os.path.join(os.path.dirname(__file__), "../../files/scripts/upload/copy_auto_%.6f" % time.time())
            obj_fp = open(string_script_name, 'wb')
            obj_fp.write(json_module_args['src'])
            obj_fp.close()
            json_module_args['src'] = string_script_name
        except Exception, e:
            pass

    if isinstance(json_module_args['src'], str):
        try:
            os.chmod(json_module_args['src'], 0755)
        except Exception, e:
            return {"success": False, "msg": e}
        obj_runner = ansible.runner.Runner(
            host_list=['127.0.0.1'],
            run_hosts=['127.0.0.1'],
            transport='local',
            module_name='copy',
            timeout=int_timeout,
            background=int_background,
            module_args="src=%s dest=%s mode=%s" % (json_module_args['src'], json_module_args['dest'], mode)
        )
        try:
            json_data = obj_runner.run()
            _stdout = json_data['contacted']['127.0.0.1']
        except Exception, e:
            return {"success": False, "msg": e}
        return {"success": True, "msg": _stdout}

    return {"success": False, "msg": u"脚本不合法"}


def remote_control_playbook(json_module_args, int_timeout=30, int_background=0):
    """
    远程shell
    参数:
        json_module_args        传递模块参数,Demo: {'playbook': 'playbook内容列表或者agent本地playbook路径'}
        int_timeout             模块运行超时
        int_background          模块是否后台运行
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    if isinstance(json_module_args['playbook'], unicode):
        json_module_args['playbook'] = json_module_args['playbook'].encode('utf8')

    if isinstance(json_module_args['playbook'], list):
        string_script_name = os.path.join(os.path.dirname(__file__), "../../files/scripts/upload/playbook_auto_%.6f" % time.time())
        obj_fp = open(string_script_name, 'w')
        for line in json_module_args['playbook']:
            obj_fp.write(line.encode('utf8'))
        obj_fp.close()
        json_module_args['playbook'] = string_script_name

    if isinstance(json_module_args['playbook'], str):
        try:
            os.chmod(json_module_args['playbook'], 0755)
        except Exception, e:
            return {"success": False, "msg": e}
        stats = ansible.callbacks.AggregateStats()
        playbook_cb = ansible.callbacks.PlaybookCallbacks(verbose=ansible.utils.VERBOSITY)
        runner_callbacks = ansible.callbacks.PlaybookRunnerCallbacks(stats, verbose=ansible.utils.VERBOSITY)
        pb = ansible.playbook.PlayBook(
            host_list=['127.0.0.1'],
            playbook=json_module_args['playbook'],
            runner_callbacks=runner_callbacks,
            stats=stats,
            callbacks=playbook_cb,
            transport='local',
            timeout=int_timeout
        )
        try:
            _re = pb.run()
            hosts = sorted(pb.stats.processed.keys())
            json_data = list()
            failed_hosts = list()
            unreachable_hosts = list()
            msg = "PLAY RECAP"
            json_data.append(msg)
            playbook_cb.on_stats(pb.stats)
            for h in hosts:
                t = pb.stats.summarize(h)
                if t['failures'] > 0:
                    failed_hosts.append(h)
                if t['unreachable'] > 0:
                    unreachable_hosts.append(h)
            retries = failed_hosts + unreachable_hosts
            if CS.RETRY_FILES_ENABLED and len(retries) > 0:
                filename = pb.generate_retry_inventory(retries)
                if filename:
                    msg = "           to retry, use: --limit @%s\n" % filename
                    json_data.append(msg)
            for h in hosts:
                t = pb.stats.summarize(h)
                _color = 'green'
                if t['changed'] > 0:
                    _color = 'yellow'
                if t['unreachable'] > 0 or t['failures'] > 0:
                    _color = 'red'
                msg = "%s : %s %s %s %s" % (
                    h + """&emsp;&emsp;""",
                    """ok=""" + str(t['ok']) + """&emsp;""",
                    """changed=""" + str(t['changed']) + """&emsp;""",
                    """unreachable=""" + str(t['unreachable']) + """&emsp;""",
                    """failures=""" + str(t['failures']) + """&emsp;"""
                )
                json_data.append(msg)

            _stdout = json_data
        except Exception, e:
            return {"success": False, "msg": e}
        return {"success": True, "msg": _stdout}

    return {"success": False, "msg": u"playbook不合法"}


def remote_control_capture(json_module_args, int_timeout=30, int_background=0):
    """
    远程抓取属性
    参数:
        json_module_args        传递模块参数,Demo: {'name': 'ansible_default_ipv4.address'},name的值为ALL则返回所有属性
        int_timeout             模块运行超时
        int_background          模块是否后台运行
    返回值:
        json                    成功失败信息与模块返回值信息
        成功：
        {
            "success": True,
            "msg": 执行返回信息
        }
        失败：
        {
            "success": False,
            "msg": 异常返回信息
        }
    """
    if isinstance(json_module_args['name'], unicode):
        json_module_args['name'] = json_module_args['name'].encode('utf8').strip()

    obj_runner = ansible.runner.Runner(
        host_list=['127.0.0.1'],
        run_hosts=['127.0.0.1'],
        transport='local',
        module_name='setup',
        timeout=int_timeout,
        background=int_background
    )
    try:
        json_data = obj_runner.run()
        _stdout = json_data['contacted']['127.0.0.1']['ansible_facts']
        if json_module_args['name'] != 'ALL':
            for _p in json_module_args['name'].split('.'):
                _stdout = _stdout[_p]

    except Exception, e:
        return {"success": False, "msg": e}

    return {"success": True, "msg": _stdout}
