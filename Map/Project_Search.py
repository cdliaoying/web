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


import requests
import re, time
from Map.Public import proj_info, parameter_search


# define function that to get the list of the project
def _get_project_list(region, kw, pn=10):
    """

    :param region: the city code where the objects inside, you can input code or name
    :param kw: the objects which you want to search
    :param pn: the page No.
    :return: the projects' attribute in the list
    """
    # define parameter
    __parameter = parameter_search()

    # define then csv file
    '''
    _csvFile = open(r'/Users/liaoying/Desktop/Python Project/Baidu/dic/%s.csv' % 'CityData', 'a+',
                    newline='', encoding='utf-8')
    _writer = csv.writer(_csvFile)
    _writer.writerow(('ID', 'project_name', 'alias', 'plate', 'p_x', 'p_y', 'add1', 'add2', 'developer', 'type',
                      'property', 'fee', 'phone'))
    '''

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
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/community', 'w')
        # f.write(_r_list[2])
        # f.close()
        '''

        for __r in __r_list:
            __project = proj_info(__r)
            __n += 1
            print("\nproj_id: %s" % __project.id)
            print("proj_name: %s" % __project.name)
            print("proj_alias: %s" % __project.alias)
            print("proj_plate: %s" % __project.plate)
            print("proj_mctX: %s" % __project.mct_x)
            print("proj_mctY: %s" % __project.mct_y)
            print("proj_add1: %s" % __project.add1)
            print("proj_add2: %s" % __project.add2)
            print("proj_dev: %s" % __project.developer)
            print("proj_type: %s" % __project.type)
            print("proj_prop_com: %s" % __project.prop_company)
            print("proj_fee: %s" % __project.prop_fee)
            print("proj_area_x: %s" % __project.pix_area_x)
            print("proj_area_y: %s" % __project.pix_area_y)
            print("proj_area_code: %s" % __project.area_code)
            print("proj_area_name: %s" % __project.area_name)
            print("base_time: %s" % __project.base_update_time)
            print("navi_time: %s" % __project.point_update_time)
            print("street_id: %s" % __project.street_id)

        __m = __n
        return __m

    except ValueError as e:
        raise e
    finally:
        pass


def _get_proj_shape(street_id):
    __p_id = street_id
    __url = "http://map.baidu.com/"
    __parameter = {
        "b": "",
        "biz": "1",
        "c": "75",
        "da_par": "direct",
        "ext_ver": "new",
        "from": "webmap",
        "ie": "utf-8",
        "l": "12",
        "newmap": "1",
        "nn": "0",
        "pcevaname": "pc4.1",
        "qt": "ext",
        "reqflag": "pcmap",
        # "t":"",
        "tn": "B_NORMAL_MAP",
        # "u_loc":"11585297, 3568091"
        "uid": __p_id,
    }
    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }
    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        __pattern = r'(?<="content":.).+?(?=.},"current_city")'
        __r_list = re.findall(__pattern, __htm_code)  # 按段落匹配

        if __r_list:
            __p1 = r'(?<=\|1-).+?(?=.","uid")'
            __r = re.findall(__p1, __r_list[0])
            __coor_str = __r[0]
            __coor_list = __coor_str.split(",")
            __m = 0
            __n = 1
            __proj_geo = []
            while __n <= len(__coor_list):
                __coor = __coor_list[__m] + "," + __coor_list[__n]
                __proj_geo.append(__coor)
                __m = __m + 2
                __n = __n + 2
        else:
            __proj_geo = None

        print(__proj_geo)
        return __proj_geo
    except ValueError as e:
        raise e
    finally:
        pass


def proj_search(region, kw, n):
    """

    :param region: the city code where the objects inside, you can input code or name
    :param kw: he objects which you want to search
    :param n: the page No.
    :return: no return
    """
    __region = region
    __kw = kw
    __n = int(n)
    __start = time.time()
    __num = 1
    __s = 0

    for page in range(__n):
        __m = _get_project_list(__region, __kw, page)  # 防止访问频率太高，避免被百度公司封
        time.sleep(2)
        if __num % 20 == 0:
            time.sleep(4)
        if __num % 100 == 0:
            time.sleep(6)
        if __num % 200 == 0:
            time.sleep(8)
        __num = __num + 1
        __s = __s + __m

    __end = time.time()
    __last_time = int((__end-__start))
    print('\n 共耗时 %s s, 获取 %s 页，%s 条数据！' % (str(__last_time), __num-1, __s))


'''
# test code
_get_project_list("631", "小区", 2)
'''

# proj_search("631", "小区", 2)
_get_proj_shape("82061b7f137f08c2ed74f823")
