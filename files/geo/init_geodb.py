#!/usr/local/baize/env/bin/python
# coding:utf-8

# (c) 2016 , Tianbiao Zu <zutianbian@qq.com>
#
# 该文件是白泽自动化管理系统的一部分,是白泽系统用于初始化geo数据库的脚本


###################################################################################################
import os
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('/usr/local/baize/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from APP.APP_web.models import Geo, Isp

BASE_DB_JSON_DIR = os.path.dirname(__file__)


def write_geodb_province(province, location):
    """ 根据省份名称生成省份geo数据库"""
    country = u"中国"
    longitude = 0
    latitude = 0
    for p in location:
        if province in p['name']:
            longitude = p['log']
            latitude = p['lat']
            geo = Geo(country=country, province=province, city='', area='', longitude=float(longitude), latitude=float(latitude))
            print u"国家: 中国，省份: %s, 经度: %s, 纬度: %s" % (province, longitude, latitude)
            try:
                geo.save()
            except Exception, e:
                pass


def write_geodb_city(province, city, location):
    """ 根据省份城市名称生成城市geo数据库"""
    country = u"中国"
    longitude = 0
    latitude = 0
    for p in location:
        if province in p['name']:
            for a in p['children']:
                if city in a['name']:
                    longitude = a['log']
                    latitude = a['lat']
            geo = Geo(country=country, province=province, city=city, area='', longitude=float(longitude), latitude=float(latitude))
            print u"国家: 中国，省份: %s, 城市: %s, 经度: %s, 纬度: %s" % (province, city, longitude, latitude)
            try:
                geo.save()
            except Exception, e:
                pass


def write_isp():
    """ 生成城市isp数据库"""
    file_isp_json = os.path.join(BASE_DB_JSON_DIR, 'isp.json')
    fp = open(file_isp_json, 'r')
    isp = json.load(fp)
    fp.close()
    for i in isp:
        if i:
            _isp = Isp(name=i)
            try:
                _isp.save()
            except Exception, e:
                pass


if __name__ == '__main__':
    write_isp()
    file_map_json = os.path.join(BASE_DB_JSON_DIR, 'map.json')
    file_location_json = os.path.join(BASE_DB_JSON_DIR, 'location.json')
    fp = open(file_map_json, 'r')
    map = json.load(fp)
    fp.close()
    fp = open(file_location_json, 'r')
    location = json.load(fp)
    fp.close()
    country = u"中国"
    for l_p in map:
        if l_p:
            province = l_p['name']
            write_geodb_province(province, location)
            for l_c in l_p['city']:
                city = l_c['name']
                write_geodb_city(province, city, location)
                for area in l_c['area']:
                    longitude = 0
                    latitude = 0
                    for loc_p in location:
                        if province in loc_p['name']:
                            for loc_a in loc_p['children']:
                                if area in loc_a['name']:
                                    longitude = loc_a['log']
                                    latitude = loc_a['lat']
                                    geo = Geo(country=country, province=province, city=city, area=area, longitude=float(longitude), latitude=float(latitude))
                                    print u"国家: 中国，省份: %s, 城市: %s, 县区: %s 经度: %s, 纬度: %s" % (province, city, area, longitude, latitude)
                                    try:
                                        geo.save()
                                    except Exception, e:
                                        pass
