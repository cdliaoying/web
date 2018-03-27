# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.25
Description:
- this procedure is helping translate the mercator to the wgs84.
- https://www.cnblogs.com/reboot777/p/7124010.html

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
        # "da_src": "pcmappg.poi.page",
        # "on_gel": "1",
        # "src": "7",
        # "gr": "3",
        # "l": "12",
        # "tn": "B_NORMAL_MAP",
        # "u_loc": "12621219.536556,2630747.285024",
        "ie": "utf-8",
        # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
        # "t": "1468896652886"
    }

    # define the url and others
    _url = 'https://map.baidu.com/'
    _parameter["c"] = region
    _parameter["wd"] = kw
    _parameter["pn"] = pn
    _parameter["nn"] = _parameter["pn"] * 10

    try:
        _htm_get = requests.get(_url, params=_parameter, timeout=6)
        print("\n the requests' status is %s \n" % _htm_get.raise_for_status())
        _htm_code = _htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        print("\n %s" % len(_htm_code))
        _pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
        _r_list = re.findall(_pattern, _htm_code)  # 按段落匹配

        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/gaode', 'w')
        f.write(_htm_code)
        f.close()

    except ValueError as e:
        raise e
    finally:
        pass


_get_project_list("青羊区", "购物中心", 0)
