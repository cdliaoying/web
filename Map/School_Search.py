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

import requests, re


def _get_project_list(region, kw, pn=10):
    # define parameter
    _parameter = {
        "newmap": "1",
        "reqflag": "pcmap",
        "biz": "1",
        "from": "webmap",
        "da_par": "direct",
        "pcevaname": "pc4.1",
        "qt": "con",
        "c": "",  # 城市代码
        "wd": "",  # 搜索关键词
        "wd2": "",
        "pn": "",  # 页数
        "nn": "",
        "db": "0",
        "sug": "0",
        "addr": "0",
        "da_src": "pcmappg.poi.page",
        "on_gel": "1",
        "src": "7",
        "gr": "3",
        "l": "12",
        "tn": "B_NORMAL_MAP",
        # "u_loc": "12621219.536556,2630747.285024",
        "ie": "utf-8",
        # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
        # "t": "1468896652886"
    }


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
        _pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
        _r_list = re.findall(_pattern, _htm_code)  # 按段落匹配

        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/Python Project/Baidu/dic/school', 'w')
        f.write(_r_list[0])
        f.close()
    except ValueError as e:
        raise e
    finally:
        pass


_get_project_list("631", "小学", 2)