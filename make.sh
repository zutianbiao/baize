#!/bin/bash

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,Baize是一款通用的DevOps系统
#
# 该文件负责Baize基础软件环境的打包
# git clone git@115.182.63.178:zutianbiao/baize_v2.git;mv baize_v2 baize;cd baize;sh make.sh
# 安装
# mkdir -p /letv/ngxlog/baize;ln -s /letv/ngxlog/baize /usr/local/baize;rm -fr /tmp/baize*;wget -SO /tmp/baize_v1.0.tar.gz "115.182.94.72/baize/baize_v1.0.tar.gz";mkdir -p /tmp/baize;tar zxvf /tmp/baize_v1.0.tar.gz -C /tmp/baize;cd /tmp/baize;sleep 3;sh manage.sh install proxy


##############################################################################
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
export PATH
mkdir -p /tmp/baize/log/
/usr/local/baize/env/bin/python manage.py migrate
/usr/local/baize/env/bin/python manage.py migrate --database=web
/usr/local/baize/env/bin/python manage.py migrate --database=agent
/usr/local/baize/env/bin/python manage.py migrate --database=proxy
tar zcvf /tmp/baize_v1.0.tar.gz ./* --exclude=*.pyc --exclude=*.log --exclude=.git --exclude=make.sh --exclude=./static
#scp /tmp/baize_v1.0.tar.gz 115.182.94.72:/var/www/html/baize/