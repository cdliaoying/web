# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.13
Description:
- this procedure is helping find the hospital in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- it has ngo problem, need translate to BaiDu Map Coordinate System. So need another Function


"""

import requests, re, time
from Map.Public import hospital_info, parameter_search


def _get_school_list(region, kw, pn=10):
    """

    :param region:
    :param kw:
    :param pn:
    :return _m:
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
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/hospital.txt', 'w')
        f.write(_r_list[3])
        f.close()
        '''
        if len(_r_list) > 0:
            for _r in _r_list:
                _hospital = hospital_info(_r)
                # add sql for insert database
                # school_write_sql(_school)
                _n += 1
                print("\n")
                print(_hospital.id, ', ', _hospital.name, ', ', _hospital.plate, ', ', _hospital.mct_x, ', ',
                      _hospital.mct_y, ', ', _hospital.add1, ', ', _hospital.add2, ', ', _hospital.type, ', ',
                      _hospital.pix_area_x, ', ', _hospital.pix_area_y, ', ', _hospital.area_code, ', ',
                      _hospital.area_name, ', ', _hospital.base_update_time, ', ', _hospital.point_update_time)

        return _n
    except ValueError as e:
        raise e
    finally:
        pass


# test code
_get_school_list("631", "医院", 4)

