#!/bin/bash

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,Baize是一款通用的DevOps系统
#
# 该文件负责Baize基础软件系统proxy agent在乐视demo的更新
#
#


##############################################################################
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
export PATH

sleep $((RANDOM%10))
rm -fr /tmp/baize*
wget -SNO /tmp/baize_v1.0.tar.gz "115.182.94.72/baize/baize_v1.0.tar.gz" > /dev/null 2>&1
mkdir -p /tmp/baize
tar zxvf /tmp/baize_v1.0.tar.gz -C /tmp/baize > /dev/null
cd /tmp/baize
sh manage.sh install proxy;sh manage.sh install agent;
LOCAL_IP=$(ifconfig|grep -a "inet addr:"|head -n 1|awk -F ':' '{print $2}'|awk '{print $1}')
sed -i "s/127.0.0.1:8101/$LOCAL_IP:8101/g" /usr/local/baize/APP/APP_agent/config.py
cat /usr/local/baize/APP/APP_agent/config.py
/etc/init.d/baize all_restart

