#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统的短信报警API, 自有内网短信网关接口


###################################################################################################
import datetime
import urllib
import urllib2

def request(url, method='POST', data={}, timeout=15):
    """ 发起http协议请求 """
    if method == 'POST':
        data = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=data)
    else:
        req = urllib2.Request(url=url)
    try:
        url_open = urllib2.urlopen(req, timeout=timeout)
        re = url_open.read()
        re = True if re.split('operresult')[1].split('>')[1].split('<')[0] == '0000' else False
    except Exception, e:
        return {"success": False, 'msg': str(e)}
    return re


def convert_message(send_string):
    """ 对消息进行编码 """
    # 获取UTF-16BE编码字符串的byte数组
    array = bytearray(send_string.decode('UTF-8').encode('UTF-16BE'))
    res = ''
    # 将数组成员转换成16进制字符，并去掉0x后组成待发送字符串
    for i in array:
        tmp = hex(i)[2:]
        if len(tmp) < 2:
            tmp = '0' + tmp
        res += tmp
    # 将待发送字符串全部大写，然后返回
    return res.upper()


def send(phone, msg):
    URL = 'http://172.16.93.6:9090/ReceiveDataFromBusinessServlet'
    stamptime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    msgcontent = convert_message(msg)
    data={
        'msgversion': 1,
        'msgtype': 1,
        'sequencenumber': stamptime,
        'sendingtype': 2,
        'msisdn': phone,
        'clientid': 'jkpt',
        'smsgatewaya1': '1018810010',
        'smsgatewaya2': '',
        'keepsession': 0,
        'bizcode': '11002',
        'reportflag': 1,
        'stamptime': stamptime,
        'msgcmd': '11',
        'msgencode': 8,
        'msgcontent': msgcontent,
        'taskmsisdnflag': 0,
        'taskid': 0,
        'expiretime': '',
        'scheduletime': '',
        'iccid': '',
        'appid': '',
        'mac': ''
    }
    return request(url=URL, data=data)

if __name__ == '__main__':
    send(phone='18611642164', msg='test')
