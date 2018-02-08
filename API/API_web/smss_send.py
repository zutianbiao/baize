#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的短信报警API


###################################################################################################
import json
import requests


def request(url, data={}, timeout=15):
    """ 发起http协议请求 """
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps(data)
    req = requests.post(url, data=data, headers=headers, timeout=timeout)
    if req.status_code == requests.codes.ok:
        response_text = json.loads(req.text)
        if response_text['respCode'] == '000000':
            return True
        else:
            return response_text
    else:
        return False


def send(phone, msg):
    # 请自行更换短信接口以及调用方法
    URL = 'http://xxxxx:8888/services/sms/sendMsg.json'
    msgcontent = json.dumps({
        "content": msg
    })
    data = {
        "mobiles": phone.split(','),
        "msgData": msgcontent,
        "platformCode": "monitor",
        "templateCode": "monitor_01"
    }
    return request(url=URL, data=data)

if __name__ == '__main__':
    print send(phone='18611642164', msg='test')
