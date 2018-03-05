# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.24
Support: 邓旭东HIT
Description:
- this procedure is helping find the project in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function


"""

import requests, re, time
from Map.Public import school_info, parameter_search


def _get_school_list(region, kw, pn=10):
    """

    :param region:
    :param kw:
    :param pn:
    :return:
    """
    # define parameter
    _parameter = parameter_search()

    # define the url and others
    _url = 'http://map.baidu.com/'
    _parameter["c"] = region
    _parameter["wd"] = kw
    _parameter["pn"] = pn
    _parameter["nn"] = _parameter["pn"] * 10

    try:
        _htm_get = requests.get(_url, params=_parameter, timeout=6)
        print("\n the requests' status is %s \n" % _htm_get.raise_for_status())
        _htm_code = _htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        _pattern = r'(?<={"acc_flag.:).+?(?="ty":)'
        _r_list = re.findall(_pattern, _htm_code)  # 按段落匹配
        _n = 0
        '''
        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/school', 'w')
        f.write(_r_list[0])
        f.close()
        '''

        for _r in _r_list:
            _school = school_info(_r)
            _n += 1
            print(_school.id, ', ', _school.name, ', ', _school.alias, ', ', _school.plate, ', ', _school.mct_x, ', ',
                  _school.mct_y, ', ', _school.add1, ', ', _school.add2, ', ', _school.type, ', ',
                  _school.pix_area_x, ', ', _school.pix_area_y)

            # add sql for insert database

        _m = _n
        return _m
    except ValueError as e:
        raise e
    finally:
        pass


def school_search(region, kw, n):
    """

    :param region:
    :param kw:
    :param n:
    :return:
    """
    _region = region
    _kw = kw
    _n = int(n)
    _start = time.time()
    _num = 1
    _s = 0

    for page in range(_n):
        _m = _get_school_list(_region, _kw, page)  # 防止访问频率太高，避免被百度公司封
        time.sleep(2)
        if _num % 20 == 0:
            time.sleep(4)
        if _num % 100 == 0:
            time.sleep(6)
        if _num % 200 == 0:
            time.sleep(8)
        _num = _num + 1
        _s = _s + _m

    _end = time.time()
    _last_time = int((_end-_start))
    print('\n 共耗时 %s s, 获取 %s 页，%s 条数据！' % (str(_last_time), _num-1, _s))


# test code
# _get_school_list("631", "小学", 0)
school_search("\n 631", "幼儿园", 2)

