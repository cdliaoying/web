# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.30
Description:
- this procedure is helping find the park in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function
- the other info maybe get from the website page, just like level of hospital


"""

import requests, re, time
from Map.Public import park_info, parameter_search


def _get_park_list(region, kw, pn=10):
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
        __pattern = r'(?<={"acc_flag").+?(?=,"view_type")'
        __r_list = re.findall(__pattern, __htm_code)  # 按段落匹配

        '''
        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/park.txt', 'w')
        f.write(_htm_code)
        f.close()
        '''
        if __r_list:
            __n = 0
            for __r in __r_list:
                __park_info = park_info(__r)
                print("\n")
                print("Id: %s" % __park_info.park_id)
                print("Name: %s" % __park_info.park_name)
                print("alias: %s" % __park_info.park_alias)
                print("plate: %s" % __park_info.park_plate)
                print("add1: %s" % __park_info.park_add1)
                print("add2: %s" % __park_info.park_add2)
                print("area_code: %s" % __park_info.park_area_code)
                print("area_name: %s" % __park_info.park_area_name)
                print("mct_x: %s" % __park_info.mct_x)
                print("mct_y: %s" % __park_info.mct_y)
                print("pix_area_x: %s" % __park_info.pix_area_x)
                print("pix_area_y: %s" % __park_info.pix_area_y)
                print("park_cla_id: %s" % __park_info.park_cla_id)
                print("park_std_id: %s" % __park_info.park_std_id)
                print("park_std_tag: %s" % __park_info.park_std_tag)
                print("info_update_date: %s" % __park_info.info_update_date)
                print("point_update_date: %s" % __park_info.point_update_date)
                __n = __n + 1
            print("\nGetting %s Records!" % __n)
        else:
            print("\nIt's get any park information!")

    except ValueError as e:
        raise e
    finally:
        pass


# test code
_get_park_list("631", "公园", 1)
