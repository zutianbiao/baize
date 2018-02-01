#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,是Baize的Django基础配置文件


###################################################################################################
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '1a0m!@9#n&f-&4ui030a-m0$r)6zae(gy!0*!gmq0ldx9u=3%r'
DEBUG = False
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'APP',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'baize.urls'
WSGI_APPLICATION = 'baize.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'default.db'),
    }
}
try:
    import APP.APP_web
    INSTALLED_APPS += ('APP.APP_web',)
    DATABASES['web'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'APP/APP_web/web.db'),
    }
except ImportError:
    pass


try:
    import APP.APP_proxy
    INSTALLED_APPS += ('APP.APP_proxy',)
    DATABASES['proxy'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'APP/APP_proxy/proxy.db'),
    }
except ImportError:
    pass
try:
    import APP.APP_agent
    INSTALLED_APPS += ('APP.APP_agent',)
    DATABASES['agent'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'APP/APP_agent/agent.db'),
    }
except ImportError:
    pass

DATABASE_ROUTERS = ['baize.db_router.App_Router', ]
LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
LOGIN_URL = '/web/login/'
LOGIN_REDIRECT_URL = '/web/login/'
LOGOUT_URL = '/web/logout/'
####################################################################################################
# 日志相关配置
# 调用示例:
#        errInfo = u'我要报警了!'
#        logger = logging.getLogger('log_file')
#        logger.error(errInfo.encode('utf8'))
#        if C.LOG_SCREEN == 'ON':
#            logger = logging.getLogger('log_screen')
#            logger.error(errInfo.encode('utf8'))
##########################
# 是否开启日志
#   示例:LOG_OPEN=['ON'|'OFF']
LOG_OPEN = 'ON'
# 日志级别
#    示例:LOG_LEVEL=['DEBUG'|'INFO'|'WARNING'|'ERROR'|'CRITICAL']
LOG_LEVEL = 'DEBUG'
# 日志文件路径
#   默认:LOG_FILE=os.path.join(os.path.dirname(__file__),'log/%s.log' % LOG_LEVEL.lower())
#   示例:LOG_FILE='/var/run/log/access.log'
LOG_FILE = os.path.join(os.path.dirname(__file__), '../log/%s.log' % LOG_LEVEL.lower())
# 是否向标准输出打印日志
#   示例:LOG_SCREEN=['ON'|'OFF']
LOG_SCREEN = 'OFF'
# 日志格式
# 示例:LOG_FORMAT = '"[%(asctime)s]" "%(pathname)s[line:%(lineno)d]" "[%(levelname)s]" "%(message)s"'
#   %(name)s                          日志记录器名称
#   %(levelno)s                       日志级别编号
#   %(levelname)s                     日志级别名称('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
#   %(pathname)s                      打印日志的代码文件路径
#   %(filename)s                      打印日志的代码文件名称
#   %(module)s                        打印日志的代码模块名称
#   %(funcName)s                      打印日志的代码函数名称
#   %(lineno)d                        打印日志的代码行号
#   %(created)f                       日志记录器产生的时间戳
#   %(relativeCreated)d               日志打印时间(毫秒)
#   %(asctime)s                       日志打印时间(可读性强例如'2016-10-11 16:00:00')
#   %(thread)d                        线程id
#   %(threadName)s                    线程名称
#   %(process)d                       进程id
#   %(message)s                       日志消息主体
LOG_FORMAT = '"[%(asctime)s]" "%(pathname)s[line:%(lineno)d]" "[%(levelname)s]" "%(message)s"'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },
    'filters': {
        'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'mail_handler': {
            'level': LOG_LEVEL,
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'screen_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'standard',
        },
        'file_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['screen_handler'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_handler'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'log_mail': {
            'handlers': ['mail_handler'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'log_screen': {
            'handlers': ['screen_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'log_file': {
            'handlers': ['file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}
####################################################################################################
# 文件上传的相关配置
##########################
# 文件上传的路径
UPLOAD_ROOT = os.path.join(os.path.join('/usr/local/baize', 'static'), 'upload')

DEFAULT_CHARSET = 'utf-8'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_PASSWORD = 'baize_test'
EMAIL_HOST_USER = 'baize_test@163.com'
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True
EMAIL_PORT = 25
ADMIN_EMAIL = 'baize_test@163.com'

# 加密算法
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# web worker工作的时间间隔
INTERVAL_WORKER = 10