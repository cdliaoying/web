# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.24
Description:
- this procedure is helping find the school in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results


"""

import requests, re, time, os, sqlite3
from Map.Public import school_info, parameter_search, _dict_factory
from Map.webkit import get_object_bd09


def __school_write_sql(school_info):
    """
    the function is used for insert the school info into the db
    :param school_info: is class from the school_info
    :return: No return
    @:type school_info: class
    """
    _school = school_info
    _dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
    _con = sqlite3.connect(_dir)
    _con.row_factory = _dict_factory
    _cur = _con.cursor()
    try:
        _cur.execute("SELECT count(Id) AS num FROM school_info WHERE Id = ?", (_school.id,))
        _r = _cur.fetchall()
        if _r[0]["num"] == 0:
            _cur.execute("INSERT INTO school_info "
                         # "(Id, Name, Alias, Plate, Address, Address2, Type, Pix_X, Pix_Y, Area_X, Area_Y) "
                         "VALUES(?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                         (_school.id, _school.name, _school.alias, _school.plate, _school.add1,
                          _school.add2, _school.cla, _school.type, _school.std_id,
                          _school.mct_x, _school.mct_y, _school.pix_area_x,
                          _school.pix_area_y, _school.area_code, _school.area_name, None, None,
                          _school.base_update_time, _school.point_update_time))
            _con.commit()
            print("%s, %s 已保存!" % (_school.id, _school.name))
        else:
            print("%s, %s 已存在!" % (_school.id, _school.name))
        _con.close()
    except ValueError as e:
        raise e
    finally:
        pass


def __get_school_list(region, kw, pn=10):
    """

    :param region:
    :param kw:
    :param pn:
    :return _m:
    """
    # define parameter
    __parameter = parameter_search()

    # define the url and others
    __url = 'http://map.baidu.com/'
    __parameter["c"] = region
    __parameter["wd"] = kw
    __parameter["pn"] = pn
    __parameter["nn"] = __parameter["pn"] * 10
    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        __pattern = r'(?<={"acc_flag.:).+?(?="ty":)'
        __r_list = re.findall(__pattern, __htm_code)  # 按段落匹配
        __n = 0
        '''
        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/school', 'w')
        f.write(_r_list[3])
        f.close()
        '''
        if len(__r_list) > 0:
            for __r in __r_list:
                __school = school_info(__r)
                __n += 1
                print("\n")
                print("id: %s" % __school.id)
                print("name: %s" % __school.name)
                print("alias: %s" % __school.alias)
                print("plate: %s" % __school.plate)
                print("mct_x: %s" % __school.mct_x)
                print("mct_y: %s" % __school.mct_y)
                print("add1: %s" % __school.add1)
                print("add2: %s" % __school.add2)
                print("cla: %s" % __school.cla)
                print("type: %s" % __school.type)
                print("std_id: %s" % __school.std_id)
                print("pix_area_x: %s" % __school.pix_area_x)
                print("pix_area_y: %s" % __school.pix_area_y)
                print("area_cdoe: %s" % __school.area_code)
                print("area_name: %s" % __school.area_name)
                print("base_update: %s" % __school.base_update_time)
                print("navi_update: %s" % __school.point_update_time)
                # insert record into db
                __school_write_sql(__school)

        return __n
    except ValueError as e:
        raise e
    finally:
        pass


def school_search(region, kw, bn, en):
    """

    :param region:
    :param kw:
    :param bn:
    :param en:
    :return:
    """
    __region = region
    __kw = kw
    __page = int(bn)
    __en = int(en)
    __start = time.time()
    __num = 1
    __s = 0

    while __page <= __en:
        __m = __get_school_list(__region, __kw, __page)  # 防止访问频率太高，避免被百度公司封

        if __m / 10 > 0:
            time.sleep(2)
            if __num % 20 == 0:
                time.sleep(4)
            if __num % 100 == 0:
                time.sleep(6)
            if __num % 200 == 0:
                time.sleep(8)
            __num = __num + 1
            __s = __s + __m
            __page = __page + 1
        else:
            __page = __en + 1

    __end = time.time()
    _last_time = int((__end-__start))
    print('\n 共耗时 %s s, 获取 %s 页，%s 条数据！' % (str(_last_time), __num-1, __s))


# test code:
# _get_school_list("631", "幼儿园", 4)

# main function:
# get the school info from web:
# school_search("620", "幼儿园", 0, 40)
# translate the mct to bd09
# get_object_bd09("school_info")

