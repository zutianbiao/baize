#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统Agent的远程控制API的测试脚本


###################################################################################################
import json
import urllib
import urllib2
###################################################################################################
TEST_YAML = '/usr/local/baize/files/scripts/test/APP_proxy/test.yaml'
TEST_SCRIPT = '/usr/local/baize/files/scripts/test/APP_proxy/test.sh'
TEST_URL = 'http://127.0.0.1:8101/proxy/remote_control/'


def request(url, method='POST', data={}, timeout=15):
    """ 发起http协议请求 """
    if method == 'POST':
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = json.loads(re)
    else:
        req = urllib2.Request(url=url)
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = json.loads(re)
    return re

if __name__ == '__main__':
    print u"远程playbook测试..."
    list_file_data = open(TEST_YAML, 'r').readlines()
    str_module_args = {"playbook": list_file_data}
    json_post_data = {"string_module_name": "playbook", "string_module_args": str_module_args, "string_agents": ["127.0.0.1:8101"]}
    json_post_data = json.loads(json.dumps(json_post_data))
    print request(TEST_URL, data=json_post_data)

    print u"远程脚本测试..."
    list_file_data = open(TEST_SCRIPT, 'r').readlines()
    str_module_args = {"script": list_file_data}
    json_post_data = {"string_module_name": "script", "string_module_args": str_module_args, "string_agents": ["127.0.0.1:8101"]}
    json_post_data = json.loads(json.dumps(json_post_data))
    print request(TEST_URL, data=json_post_data)

    print u"远程copy测试..."
    list_file_data = open(TEST_SCRIPT, 'r').readlines()
    str_module_args = {"src": list_file_data, "dest": "/tmp/hostname.sh", "mode": 755}
    json_post_data = {"string_module_name": "copy", "string_module_args": str_module_args, "string_agents": ["127.0.0.1:8101"]}
    json_post_data = json.loads(json.dumps(json_post_data))
    print request(TEST_URL, data=json_post_data)

    print u"远程命令测试..."
    str_module_args = {"command": "hostname"}
    json_post_data = {"string_module_name": "shell", "string_module_args": str_module_args, "string_agents": ["127.0.0.1:8101"]}
    json_post_data = json.loads(json.dumps(json_post_data))
    print request(TEST_URL, data=json_post_data)

    print u"远程属性抓取测试..."
    str_module_args = {"name": "ansible_hostname"}
    json_post_data = {"string_module_name": "capture", "string_module_args": str_module_args, "string_agents": ["127.0.0.1:8101"]}
    json_post_data = json.loads(json.dumps(json_post_data))
    print request(TEST_URL, data=json_post_data)

