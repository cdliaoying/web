# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.28
Description:
- this procedure is helping find the metro station in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function


"""


import requests, re
from Map.Public import matro_line_info, station_info


def __get_line_info():
    """

    :return _m:
    """
    # define parameter
    __parameter = {
        "c": "75",
        "newmap": "1",
        "qt": "bsl",
        "tps": "",
        "uid": "d4d33fd4eab8d63de215f9b0",  # 1号线id
    }

    # define the url and others
    __url = 'http://map.baidu.com/'

    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        __pattern = r'(?<="kindtype":).+?(?="current_city":)'
        __r_line = re.findall(__pattern, __htm_code)  # 按段落匹配
        __pattern = r'(?<="stations":).+?(?=,"ticketPrice":)'
        __r_st = re.findall(__pattern, __htm_code)
        __pattern = r'(?<="geo":).+?(?=},{"geo":)'
        __r_station = re.findall(__pattern, __r_st[0])

        if __r_line:
            __line_info = matro_line_info(__r_line[0])
            __flag = '1'
            # add sql for insert database
            # school_write_sql(_school)
            print("\n")
            print("line_id:%s " % __line_info.line_id)
            print("line_name:%s " % __line_info.line_name)
            print("max_price:%s " % __line_info.max_price)
            print("line_tiem:%s " % __line_info.line_time)
            print("line_color:%s " % __line_info.line_color)
        else:
            __flag = '0'

        if __flag == '1' and __r_station:
            for __r in __r_station:
                __station_info = station_info(__r)
                print("\n")
                print("station_id:%s " % __station_info.st_id)
                print("station_name:%s " % __station_info.st_name)
                print("station_start_time:%s " % __station_info.st_start_time)
                print("station_end_time:%s " % __station_info.st_end_time)
                print("station_subway:%s " % __station_info.st_subway)
                print("station_transfer:%s " % __station_info.st_transfer)
                print("station_pix_x:%s " % __station_info.st_pix_x)
                print("station_pix_y:%s " % __station_info.st_pix_y)

    except ValueError as e:
        raise e
    finally:
        pass


__get_line_info()
