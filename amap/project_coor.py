# -*- coding: UTF-8 -*-

"""

Author: Wayne
Ver: v0.0.1
Date: 2018.05.04
Description:
- this procedure is using for find the coordinate of project by the API of amap.

"""

import requests, re, os, datetime, time
import cx_Oracle as oracle
from amap import amp_class
from support.distance import coor_dis


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # globe setting


def __addr_2_coor(address: str, datasource: str):
    """ this is api of amap map webservice to translate the name or address of project to amap's coordinate

    :param:
      address {str} - can instead of name, the two of key argument of project;
      datasource {str} - the code of region, to confirm the result from amap whether is in the region
      __parameters["city"] {str} - not include in the input ,but need changing in the other city

    :return:
        __flag {str} - it's a boolean object, it's a judgement of writing data
        __coor_x {str} - the point's lng from api
        __coor_y {str} - the point's lat from api

    """
    __info = amp_class.connection()
    __parameters = {"key": __info.geo_key,
                    "address": "",
                    "city": "成都市",
                    "output": "jason"}

    __url = __info.geo_url
    __parameters["address"] = address
    __coor_x = ''
    __coor_y = ''
    __flag = ''

    try:
        __response_get = requests.get(__url, params=__parameters, timeout=6)
        print("the connection is... %s" % __response_get.raise_for_status())
        __proj_j = __response_get.json()

        if __proj_j["status"] == '1':
            for __r in __proj_j["geocodes"]:
                __proj_r = amp_class.proj(__r)
                if __proj_r.adcode == datasource:
                    # print("\n victory")
                    # print(__proj_r.address)
                    # print(__proj_r.province)
                    # print(__proj_r.adcode)
                    # print(__proj_r.district)
                    # print(__proj_r.street)
                    # print(__proj_r.location)
                    __coor_list = re.split(r',', __proj_r.location)
                    if __coor_list:
                        __flag = '1'
                        __coor_x = __coor_list[0]
                        __coor_y = __coor_list[1]
                        print("需要更新！")
                    else:
                        __flag = '0'
                        __coor_x = None
                        __coor_y = None
                        print("不需要更新！")
                else:
                    __flag = '0'
                    __coor_x = None
                    __coor_y = None
                    print("不需要更新！")
        return __flag, __coor_x, __coor_y
    except Exception as e:
        raise e
    finally:
        pass


def __rows_as_dicts(cursor):
    """ used for format results list from list to dict

    :param
        cursor {list} - the result from oracle

    :return:
        dict - the result after format

    """
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]


def __get_project(region: str, data_source: str):
    """ the main function, include three part: 1st is getting objects from oracle; 2nd is getting flag and coordinate
            by the api of amap, 3rd is update data and compute the distances of name and address' coordinates

    :param:
        region {str} - the name of region
        data_source {str} - the code of region
    :return:
        any
    """
    __connect = {
        "host": "172.29.251.71",
        "port": "1521",
        "sid": "orcl",
        "account": "assessprice",
        "psw": "assessprice",
    }
    __region_name = region
    __region_code = data_source
    try:
        __dsn = oracle.makedsn(__connect["host"], __connect["port"], __connect["sid"])
        __conn = oracle.connect(__connect["account"], __connect["psw"], __dsn)
        __cursor = __conn.cursor()
        __cursor.prepare("SELECT ID, PROJECT_NAME, GD_NAME, LJ_NAME, DISTRICT_ADD, "
                         "REGION, ADD_LNG, ADD_LAT, NAME_LNG, NAME_LAT "
                         "FROM ASSESSPRICE.TMP_LJ_DISTRICT_REL "
                         "WHERE REGION =:region")
        __cursor.execute(None, {"region": __region_name})
        __data = __rows_as_dicts(__cursor)
        __m = len(__data)
        __n = 0

        for __d in __data:
            __r = amp_class.or_proj(__d)
            __addr = "%s%s" % (__region_name, __r.ds_addr)
            __flag, __p_lng, __p_lat = __addr_2_coor(__addr, __region_code)
            if __flag == '1':
                __update_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                __fid = __r.r_id
                __distance = coor_dis(__r.name_lng, __r.name_lat, __r.addr_lng, __r.addr_lat)
                print(__r.r_id, __r.pj_name, __r.ds_addr, __r.addr_lng, __r.addr_lat, __p_lng, __p_lat, __distance)
                print("\n")
                __cursor.prepare("UPDATE ASSESSPRICE.TMP_LJ_DISTRICT_REL "
                                 "SET ADD_LNG = :addr_lng, ADD_LAT = :addr_lat, DISTANCE = :distance, "
                                 "SYS_UPDATE_TIME = to_date(:update_time,'yyyy-mm-dd hh24:mi:ss')"
                                 "WHERE ID = :fid")
                __cursor.execute(None, {"addr_lng": __p_lng, "addr_lat": __p_lat,
                                        "distance": __distance, "update_time": __update_date,
                                        "fid": __fid})
                __conn.commit()
                __n = __n + 1
                if __n == 1000:
                    time.sleep(20)
                    print("等待20s！")
                else:
                    time.sleep(0.2)

        __cursor.close()
        __conn.close()
        print("执行完成！%s 共 %s 条数据, 更新 %s 条！" % (__region_name, __m, __n))
    except Exception as e:
        raise e
    finally:
        pass


if __name__ == "__main__":
    # lat, lng = __addr_2_coor("三河叠秀路108号", "510114")
    __get_project("青羊区", "510105")
