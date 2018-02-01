#!/usr/local/baize/env/bin/python
#coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@163.com>
#
# 该文件是Baize的一部分,是Baize的Django manage文件


###################################################################################################
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
