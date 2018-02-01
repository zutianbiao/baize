#!/bin/bash
# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该脚本用于执行Baize的web端数据备份
# Baize是一个DevOps系统
#
##############################################################################
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
export PATH

###################[ 日志相关配置 ]###########################################
# 是否打开debug日志[1/0]代表[打开/关闭]
DEBUG=1
# debug日志位置
PATH_DEBUG_LOG='/tmp/baize_db_backup.log'

###################[ 备份数据相关配置 ]####################################
TIME_NOW=$(date '+%Y%m%d%H%M%S')
# 备份资源的目标路径
DIR_BACKUP='/usr/local/baize/db_backup/'
LIST_BACKUP_CONF=(\
"web数据库 /usr/local/baize/APP/APP_web/web.db /usr/local/baize/db_backup/web_$TIME_NOW.db 644" \
"default数据库 /usr/local/baize/default.db /usr/local/baize/db_backup/default_$TIME_NOW.db 644" \
)

##############################################################################
# 函数 write_log()
# 功能 打印日志
# 参数:
#      $1    日志级别[Error|OK]
#      $2    日志内容
# 返回值:
#      无
#
###############################################################################
function write_log(){
    if [ $DEBUG -ne 0 ];then
        echo "[$1]:    $2"
    fi
}
#############################################################################
# 函数 file_install_single()
# 功能 Baize工程单一文件安装
# 参数:
#    $1    脚本的中文名称
#    $2    脚本存放的源路径
#    $3    脚本存放的目标路径
#    $4    脚本的权限代码,例如755
# 返回值:
#    打印成功失败信息,并返回[0/1]代表[成功/失败]
#############################################################################
function file_install_single(){
    mkdir -p $(dirname $3)
    if [ -f $3 ];then
        md5_now=`md5sum $3|awk '{print $1}'`
        md5_old=`md5sum $2|awk '{print $1}'`
        if [ "$md5_now"x == "$md5_old"x ];then
            chmod $4 $3 >> ${PATH_DEBUG_LOG} 2>&1
            write_log "OK" "$1$3备份成功"
            return 0
        else
            \cp -f $2 $3 >> ${PATH_DEBUG_LOG} 2>&1
            chmod $4 $3 >> ${PATH_DEBUG_LOG} 2>&1
        fi
    else
        \cp -f $2 $3 >> ${PATH_DEBUG_LOG} 2>&1
        chmod $4 $3 >> ${PATH_DEBUG_LOG} 2>&1
    fi
    if [ -f $3 ];then
        write_log "OK" "$1$3备份成功"
        return 0
    else
        write_log "Error" "$1$3备份失败,debug日志:${PATH_DEBUG_LOG}"
        return 1
    fi
}

for((i=0;i<${#LIST_BACKUP_CONF[@]};i++))
do
    file_now=(${LIST_BACKUP_CONF[$i]})
    file_install_single ${file_now[0]} ${file_now[1]} ${file_now[2]} ${file_now[3]}
    # ll --sort=time ${DIR_BACKUP}|awk '{if(NR>500){system("rm -f '"${DIR_BACKUP}"'" $9)}}'
done

