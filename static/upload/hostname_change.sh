#!/bin/bash

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,Baize是一款通用的DevOps系统
#
# 该文件是Baize远程设置主机名的脚本

##############################################################################
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
export PATH

##################################################################
# 函数 hostname_change()
# 功能 修改主机名
# 参数:
#      $1    修改后的主机名
# 返回值:
#      无
#
##################################################################
function hostname_change() {
    HOSTNAME=$1
    export HOSTNAME
    sed -i '/HOSTNAME/d' /etc/sysconfig/network
    echo "HOSTNAME=${HOSTNAME}" >>/etc/sysconfig/network
    if [ -z "`cat /etc/hosts | grep $HOSTNAME | grep 127.0.0.1`" ]
    then
            sed -i "s/^127.0.0.1.*/& $HOSTNAME/" /etc/hosts
    fi
    hostname ${HOSTNAME}
}
hostname_change $@
echo "更新完成: $(hostname)"