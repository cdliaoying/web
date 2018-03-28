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


def _get_project_list():
    # define parameter
    _parameter = {
        "c": "75",
        "newmap": "1",
        "qt": "bsl",
        "tps": "",
        "uid": "d4d33fd4eab8d63de215f9b0", # 1号线id
    }

    # define the url and others
    _url = 'https://map.baidu.com/'

    try:
        _htm_get = requests.get(_url, params=_parameter, timeout=6)
        print("\n the requests' status is %s \n" % _htm_get.raise_for_status())
        _htm_code = _htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        print("\n %s" % len(_htm_code))
        _pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
        _r_list = re.findall(_pattern, _htm_code)  # 按段落匹配

        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/metro', 'w')
        f.write(_htm_code)
        f.close()

    except ValueError as e:
        raise e
    finally:
        pass


_get_project_list()
