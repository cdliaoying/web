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
import re, csv, time
from Map.Public import proj_info


# define function that to get the list of the project
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

    # define then csv file
    _csvFile = open(r'/Users/liaoying/Desktop/Python Project/Baidu/dic/%s.csv' % 'CityData', 'a+',
                    newline='', encoding='utf-8')
    _writer = csv.writer(_csvFile)
    _writer.writerow(('ID', 'project_name', 'alias', 'plate', 'p_x', 'p_y', 'add1', 'add2', 'developer', 'type',
                      'property', 'fee', 'phone'))

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
        f = open('/Users/liaoying/Desktop/Python Project/Baidu/dic/community', 'w')
        # f.write(_r_list[2])
        # f.close()
        '''

        for _r in _r_list:
            _project = proj_info(_r)
            _n += 1
            print(_project.id, ', ', _project.name, ', ', _project.alias, ', ', _project.plate, ', ', _project.mct_x,
                  ', ', _project.mct_y, ', ', _project.add1, ' ', _project.add2, ' ', _project.developer, ', ',
                  _project.type, ', ', _project.prop_company, ', ', _project.prop_fee, ', ', _project.pix_area_x,
                  ', ', _project.pix_area_y)

        _m = _n
        return _m

    except ValueError as e:
        raise e
    finally:
        pass


def proj_search(region, kw, n):
    _region = region
    _kw = kw
    _n = int(n)
    _start = time.time()
    _num = 1
    _s = 0

    for page in range(_n):
        _m = _get_project_list(_region, _kw, page)  # 防止访问频率太高，避免被百度公司封
        time.sleep(2)
        if _num % 20 == 0:
            time.sleep(4)
        if _num % 100 == 0:
            time.sleep(6)
        if _num % 200 == 0:
            time.sleep(8)
        _num = _num + 1
        _s = _s + _m

    _end = time.time()
    _last_time = int((_end-_start))
    print('\n 共耗时 %s s, 获取 %s 页，%s 条数据！' % (str(_last_time), _num-1, _s))


'''
# test code
_get_project_list("631", "小区", 2)
'''

proj_search("631", "小区", 2)
