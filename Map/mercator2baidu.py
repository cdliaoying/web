# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.25
Description:
- this procedure is helping translate the mercator to the wgs84.
- https://www.cnblogs.com/reboot777/p/7124010.html

"""

import math

pi = 3.14159265358979324
a = 6378245.0
ee = 0.00669342162296594323


# 墨卡托投影坐标转经纬度坐标
def _mercator_2_wgs84(mercator):
    _point_x = mercator[0]
    _point_y = mercator[1]
    _x = _point_x / 20037508.3427892 * 180
    _y = _point_y / 20037508.3427892 * 180
    _y = 180 / math.pi * (2 * math.atan(math.exp(_y * math.pi / 180)) - math.pi / 2)
    _m2w = dict(lat=_y, lon=_x)
    return _m2w


# test the point weather in the China
def _out_of_china(lat, lon):
    """
       判断是否在国内，不在国内不做偏移
       :param lon:
       :param lat:
       :return:
       """
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def _trans_form_lat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def _trans_form_lng(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


def _wgs84_2_mars(wgLat, wgLon):
    _mars_point = dict(lat=0, lon=0)
    if _out_of_china(wgLat, wgLon):
        _mars_point["lat"] = wgLat
        _mars_point["lon"] = wgLon
    else:
        _dLat = _trans_form_lat(wgLon - 105.0, wgLat - 35.0)
        _dLon = _trans_form_lng(wgLon - 105.0, wgLat - 35.0)
        _radLat = wgLat / 180.0 * pi
        _magic = math.sin(_radLat)
        _magic = 1 - ee * _magic * _magic
        _sqrtMagic = math.sqrt(_magic)
        _dLat = (_dLat * 180.0) / ((a * (1 - ee)) / (_magic * _sqrtMagic) * pi)
        _dLon = (_dLon * 180.0) / (a / _sqrtMagic * math.cos(_radLat) * pi)
        _mars_point["lat"] = wgLat + _dLat
        _mars_point["lon"] = wgLon + _dLon
    return _mars_point


def _mars_2_baidu(mars_point):
    _x_pi = 3.14159265358979324 * 3000.0 / 180.0
    _baidu_point = dict(lon=0, lat=0)
    _x = mars_point["lon"]
    _y = mars_point["lat"]
    _z = math.sqrt(_x * _x + _y * _y) + 0.00002 * math.sin(_y * _x_pi)
    _theta = math.atan2(_y, _x) + 0.000003 * math.cos(_x * _x_pi)
    _baidu_point["lon"] = _z * math.cos(_theta) + 0.0065
    _baidu_point["lat"] = _z * math.sin(_theta) + 0.006
    return _baidu_point


# test code: 成都市鼓楼小学: baidu: 104.080471,30.670996, mars: 104.074498,30.664996
mercator = (11586260.2779, 3568139.31197)
m2w = _mercator_2_wgs84(mercator)
print("\n wgs84 is (lon = %s,lat = %s)" % (m2w["lon"], m2w["lat"]))
print("\n the point out of China: %s " % _out_of_china(m2w["lat"], m2w["lon"]))
mars_point1 = _wgs84_2_mars(m2w["lat"], m2w["lon"])
print("\n mars is (lon = %s,lat = %s)" % (mars_point1["lon"], mars_point1["lat"]))
mars_point = dict(lon=104.074498, lat=30.664996)
baidu_point = _mars_2_baidu(mars_point1)
print("\n baidu is (lon = %s,lat = %s)" % (baidu_point["lon"], baidu_point["lat"]))
