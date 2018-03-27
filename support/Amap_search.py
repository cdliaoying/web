# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.03.27
Description:
- this file is an experiment for the get some message from ditu.amap.com
- https://zhuanlan.zhihu.com/p/25713752

"""

import requests, re

__url = 'https://ditu.amap.com/service/poiInfo'
__parameter = {
    "addr_poi_merge": "true",
    "city": "510100",
    "cluster_state": "5",
    "div": "PC1000",
    "geoobj": "104.062466|30.663556|104.07033|30.66651",
    "is_classify": "true",
    "keywords": "龙泉驿+小学",
    "need_utd": "true",
    "pagenum": "1",
    "pagesize": "20",
    "qii": "true",
    "query_type": "TQUERY",
    "utd_sceneid": "1000",
    "zoom": "17",
}
__headers = {
    "Host": "ditu.amap.com",
    "Referer": "https://ditu.amap.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
}

__htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
__htm_text = __htm_get.text
print("\n %s" % len(__htm_text))
__pattern = r'(?<="rating").+?(?="discount_flag")'
__r_list = re.findall(__pattern, __htm_text)  # 按段落匹配
__pattern = r'(?<="name":.).+?(?=",)'
__school_name = re.findall(__pattern, __r_list[0])
print("school_name is: %s" % __school_name[0])

"""
f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/gaode', 'w')
f.write(__htm_get.text)
f.close()
"""
