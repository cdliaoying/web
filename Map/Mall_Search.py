# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.27
Description:
- this procedure is helping find the shopping mall in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function


"""

import requests, re
from Map.Public import mall_info, parameter_search


def __get_mall_list(region, kw, pn=10):
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

    try:
        __htm_get = requests.get(__url, params=__parameter, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        __pattern = r'(?<={"acc_flag.:).+?(?="ty":)'
        __r_list = re.findall(__pattern, __htm_code)  # 按段落匹配
        __n = 0
        '''
        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/hospital.txt', 'w')
        f.write(_r_list[3])
        f.close()
        '''
        if len(__r_list) > 0:
            for __r in __r_list:
                __mall = mall_info(__r)
                # add sql for insert database
                # school_write_sql(_school)
                __n += 1
                print("\n")
                print(__mall.id, ', ', __mall.name, ', ', __mall.plate, ', ', __mall.mct_x, ', ',
                      __mall.mct_y, ', ', __mall.add1, ', ', __mall.add2, ', ', __mall.type, ', ',
                      __mall.pix_area_x, ', ', __mall.pix_area_y, ', ', __mall.area_code, ', ',
                      __mall.mall_hours, ', ', __mall.mall_floor, ', ',
                      __mall.area_name, ', ', __mall.base_update_time, ', ', __mall.point_update_time)

        return __n
    except ValueError as e:
        raise e
    finally:
        pass


# test code
__get_mall_list("631", "购物中心", 0)

