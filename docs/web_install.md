# 客户端安装

## 该部分包含baize系统web端安装方法


### 安装前须知

```
1. 白泽客户端程序默认安装到/usr/local/baize目录
2. 为保证白泽客户端正常运行/usr/local/baize目录至少10G空间(空间不足可ln -s自行创建软连接)
3. 安装过程依赖本地yum环境,需要保证可用
4. 安装过程中需要使用pip安装python环境依赖,请确保服务器可以连通公网(或者可以使用代理连通公网pip 代理可以在files/scripts/bash_lib_baize中配置)
5. baize是标准的django项目，github上的版本默认使用了sqlite数据库，支持的并发比较小，大家根据实际需求自行修改(配置文件为baize/settings.py)
```

### 下载安装包

```
cd /tmp
git clone https://github.com/zutianbiao/baize.git
```

### 修改管理员邮箱信息

```
cd /tmp/baize
vim baize/settings.py
###################################################
# 修改成自己注册的可用邮箱(该邮箱可供测试使用)
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_PASSWORD = 'baizetest123'
EMAIL_HOST_USER = 'baize_test@163.com'
SERVER_EMAIL = EMAIL_HOST_USER
# EMAIL_USE_TLS = True
EMAIL_PORT = 25
ADMIN_EMAIL = 'baize_test@163.com'
###################################################
执行命令 sh manage.sh install web安装即可
```


### 新建用户

```
# 安装完成后，使用下面命令自行创建用户
# 用户的密码将使用上面配置的邮箱发到用户邮箱中
# 平台部分操作需要django的超级管理员权限,请进入数据库自行添加权限
/usr/local/baize/env/bin/python /usr/local/baize/API/API_web/scripts/register.py 用户名 邮箱
```

### 进入系统

```
浏览器访问http://本地ip:8101/web/index即可，此处的8101端口是默认值,可以自行修改本地nginx配置
```
### 声明
```
由于代码开源，部分敏感信息较多的功能被删掉了，实际生产环境部署的时候也有很多灵活的方式。有兴趣的同学可以加一下微信群详细讨论
```