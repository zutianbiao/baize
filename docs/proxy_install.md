# proxy安装

## 该部分包含baize系统proxy安装方法


### 安装前须知

```
1. 白泽客户端程序默认安装到/usr/local/baize目录
2. 为保证白泽客户端正常运行/usr/local/baize目录至少10G空间(空间不足可ln -s自行创建软连接)
3. 安装过程依赖本地yum环境,需要保证可用
4. 安装过程中需要使用pip安装python环境依赖,请确保服务器可以连通公网(或者可以使用代理连通公网pip 代理可以在files/scripts/bash_lib_baize中配置)
```

### 下载客户端

```
cd /tmp
git clone https://github.com/zutianbiao/baize.git
```

### 手工指定web server

```
vim /tmp/baize/APP/APP_proxy/config.py
##################################################################
# 仅修改下面配置指定管理该proxy的web server即可
#
# WEB_SERVER = '172.16.211.67:8101'
#
##################################################################
```


### 安装proxy

```
cd /tmp/baize
sh manage.sh install proxy
```


