#!/bin/bash

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,Baize是一款通用的DevOps系统
#
# 该文件负责Baize基础软件环境的安装


##############################################################################
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
export PATH

. ./files/scripts/bash_lib_baize

case $1 in
    update)
        case $2 in
            web|proxy|master|agent|demo)
                LANG="zh_CN.UTF-8"
                file_bakcup
                python_install
                virtualenv_install
                env_install
                pip_update
                env_django_install
                env_ansible_install
                env_webscraping_install
                env_uwsgi_install
                env_gevent_install
                env_pycurl_install
                env_influxdb_install
                if [ "$2" == "proxy" ];then
                    influxdb_install
                fi
                dir_create
                file_install $2
                scripts_install
                nginx_install
                file_recover
                local_ip=$(/usr/local/baize/env/bin/ansible localhost -m setup -a "filter=ansible_all_ipv4_addresses"|tail -n 6|head -n 1|awk -F '"' '{print $2}')
                sed -i "s#127.0.0.1:8101#${local_ip}:8101#g" /usr/local/baize/APP/APP_agent/config.py >> ${PATH_DEBUG_LOG} 2>&1
                sed -i "s#local_ip#${local_ip}#g" /usr/local/baize/baize/settings.py >> ${PATH_DEBUG_LOG} 2>&1
                systemctl daemon-reload > /dev/null 2>&1
                /etc/init.d/baize restart
                sed -i '/baize/d' /var/spool/cron/root >> ${PATH_DEBUG_LOG} 2>&1
                if [ "$2" == "proxy" ];then
                    /etc/init.d/influxdb restart
                    /etc/init.d/baize -s baize_auto_worker_proxy_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_proxy > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                if [ "$2" == "agent" ];then
                    fact_install
                    /etc/init.d/baize -s baize_auto_worker_agent_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_agent > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                if [ "$2" == "web" ];then
                    /etc/init.d/baize -s baize_auto_worker_web_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_web > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                cron_install
                if [ "$2" == "web" ];then
                # 第一次安装web环境时由于缺少编译环境需要先执行install web
                # 然后执行make脚本
                # 再重新执行install web
                    echo "0 2 */1 * * sh /usr/local/baize/API/API_web/scripts/db_backup.sh > /dev/null 2>&1" >> /var/spool/cron/root
                #    /usr/local/baize/env/bin/python /usr/local/baize/files/geo/init_geodb.py
                fi
                ;;
            *)
                echo "请指定安装角色"
                ;;
        esac
        ;;
    install)
        case $2 in
            web|proxy|master|agent|demo)
                yum -y install gcc libcurl-devel zlib-devel openssl-devel sqlite-devel bc >> ${PATH_DEBUG_LOG} 2>&1
                sed -i '/net.core.somaxconn/d' /etc/sysctl.conf >> ${PATH_DEBUG_LOG} 2>&1
                echo "net.core.somaxconn = 60000" >> /etc/sysctl.conf
                sysctl -p >> ${PATH_DEBUG_LOG} 2>&1
                LANG="zh_CN.UTF-8"
                python_install
                virtualenv_install
                env_install
                pip_update
                env_django_install
                env_ansible_install
                env_webscraping_install
                env_uwsgi_install
                env_gevent_install
                env_pycurl_install
                env_influxdb_install
                if [ "$2" == "proxy" ];then
                    influxdb_install
                fi
                dir_create
                file_install $2
                scripts_install
                nginx_install
                local_ip=$(/usr/local/baize/env/bin/ansible localhost -m setup -a "filter=ansible_all_ipv4_addresses"|tail -n 6|head -n 1|awk -F '"' '{print $2}')
                sed -i "s#127.0.0.1:8101#${local_ip}:8101#g" /usr/local/baize/APP/APP_agent/config.py >> ${PATH_DEBUG_LOG} 2>&1
                sed -i "s#local_ip#${local_ip}#g" /usr/local/baize/baize/settings.py >> ${PATH_DEBUG_LOG} 2>&1
                systemctl daemon-reload > /dev/null 2>&1
                if [ "$2" == "proxy" ];then
                    /etc/init.d/influxdb restart
                    /etc/init.d/baize -s baize_auto_worker_proxy_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_proxy > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                if [ "$2" == "agent" ];then
                    fact_install
                    /etc/init.d/baize -s baize_auto_worker_agent_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_agent > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                if [ "$2" == "web" ];then
                    /usr/local/baize/env/bin/python manage.py migrate >> ${PATH_DEBUG_LOG} 2>&1
                    /usr/local/baize/env/bin/python manage.py migrate --database=web >> ${PATH_DEBUG_LOG} 2>&1
                    /etc/init.d/baize -s baize_auto_worker_web_restart
                    echo "* * * * * /etc/init.d/baize -s auto_restart_check_auto_worker_web > /dev/null 2>&1" >> /var/spool/cron/root
                fi
                /etc/init.d/baize restart
                sed -i '/baize/d' /var/spool/cron/root >> ${PATH_DEBUG_LOG} 2>&1
                cron_install
                if [ "$2" == "web" ];then
                    echo "0 2 */1 * * sh /usr/local/baize/API/API_web/scripts/db_backup.sh > /dev/null 2>&1" >> /var/spool/cron/root
                #    /usr/local/baize/env/bin/python /usr/local/baize/files/geo/init_geodb.py
                fi
                ;;
            *)
                echo "请指定安装角色"
                ;;
        esac
        ;;
    uninstall)
        /etc/init.d/baize stop
        rm -fr /usr/local/baize/
        sed -i '/baize/d' /var/spool/cron/root
        /etc/init.d/baize -s baize_auto_worker_proxy_stop
        /etc/init.d/influxdb stop
        /etc/init.d/baize -s baize_auto_worker_agent_stop
        rm -f /etc/init.d/baize
        rm -fr /root/.ansible/ansible_plugins/callback_plugins/*baize*
        rm -fr /tmp/baize*
        echo "卸载完毕"
        ;;
    *)
        echo "Usage: sh manage.sh [install|update|uninstall] [web|proxy|master|agent]"
        ;;
esac
