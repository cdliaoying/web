# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.24
Support: 邓旭东HIT
Description:
- this procedure is helping find the school in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function


"""

import requests, re, time
from Map.Public import school_info, parameter_search, school_write_sql


def _get_school_list(region, kw, pn=10):
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
                print(__school.id, ', ', __school.name, ', ', __school.alias, ', ', __school.plate, ', ',
                      __school.mct_x, ', ', __school.mct_y, ', ', __school.add1, ', ', __school.add2, ', ',
                      __school.cla, ', ', __school.type, ', ', __school.std_id, ', ',
                      __school.pix_area_x, ', ', __school.pix_area_y, ', ',
                      __school.area_code, ', ', __school.area_name, ', ',
                      __school.base_update_time, ', ', __school.point_update_time)
                # add sql for insert database
                school_write_sql(__school)

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
        __m = _get_school_list(__region, __kw, __page)  # 防止访问频率太高，避免被百度公司封

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
# school_search("简阳市", "小学", 0, 20)

