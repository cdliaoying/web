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
        _pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
        _r_list = re.findall(_pattern, _htm_code)  # 按段落匹配

        '''
        # 将输出结果写入文件，帮助正则式分析
        f = open('/Users/liaoying/Desktop/Python Project/Baidu/dic/community', 'w')
        # f.write(_r_list[2])
        # f.close()
        '''

        for _r in _r_list:
            # 查找小区name
            _pattern = r'(?<=\b"\},"name":").+?(?=")'
            _pj_name = re.findall(_pattern, _r)
            if not _pj_name:
                _pattern = r'(?<=\b,"name":").+?(?=")'
                _pj_name = re.findall(_pattern, _r)
            _r_pjname = _pj_name[0]

            # 查找小区alias
            _pattern = r'(?<=alias.:.).+?(?=])'
            _alias = re.findall(_pattern, _r)
            if not _alias:
                _r_alias = "Null"
            else:
                _r_alias = _alias[0]

            # 查找项目地址
            _pattern = r'(?<=poi_address.:.).+?(?=")'
            _address = re.findall(_pattern, _r)
            _add1 = _address[0]
            _pattern = r'.+?(?=")'
            adr = re.findall(_pattern, _r)
            _pattern = r'\(.+?\['
            _address = re.sub(_pattern, '', adr[0])
            _pattern = r'\(.+?\]'
            _add2 = re.sub(_pattern, '', _address)

            # 查找小区developers
            _pattern = r'(?<=developers.:.).+?(?=")'
            _developer = re.findall(_pattern, _r)
            if not _developer:
                _r_dev = "Null"
            else:
                _r_dev = _developer[0]

            # 查找小区坐标x,y
            _pattern = r'(?<=navi_x.:.).+?(?=")'
            _navi_x = re.findall(_pattern, _r)
            _r_x = _navi_x[0]
            _pattern = r'(?<=navi_y.:.).+?(?=")'
            _navi_y = re.findall(_pattern, _r)
            _r_y = _navi_y[0]

            # 查找小区tag
            _pattern = r'(?<=std_tag.:.).+?(?=")'
            _std_tag = re.findall(_pattern, _r)
            _r_tag = _std_tag[0]

            # 查找小区tag
            _pattern = r'(?<=primary_uid.:.).+?(?=")'
            _primary_uid = re.findall(_pattern, _r)
            _r_ID = _primary_uid[0]

            # 查找小区aoi
            _pattern = r'(?<=aoi.:.).+?(?=")'
            _aoi = re.findall(_pattern, _r)
            _r_aoi = _aoi[0]
            _r_aoi = re.sub(r'",', 'Null', _r_aoi)

            # 查找小区property
            _pattern = r'(?<=property_company.:.).+?(?=")'
            _property_company = re.findall(_pattern, _r)
            # _property_company = re.sub(r'",', "", _property_company)
            _r_prop_compy = _property_company[0]
            _r_prop_compy = re.sub(r'",', 'Null', _r_prop_compy)
            _pattern = r'(?<=property_management_fee.:.).+?(?=")'
            _property_management_fee = re.findall(_pattern, _r)
            # _property_management_fee = re.sub(r'",', "", _property_management_fee)
            _r_prop_fee = _property_management_fee[0]
            _r_prop_fee = re.sub(r'",', 'Null', _r_prop_fee)

            # 查找项目电话
            _pattern = r'(?<="phone":").+?(?=")'
            _phone = re.findall(_pattern, _r)
            _r_phone = _phone[0]
            _r_phone = re.sub(r'",', 'null', _r_phone)
            # print(phone[0])  # 电话

            '''
            print(_r_pjname, ' ', _r_alias, ' ', _r_aoi, ' ', _r_x, ' ', _r_y, ' ', _add1, ' ', _add2, ' ', _r_dev, ' ',
                  _r_tag, ' ', _r_prop_compy, ' ', _r_prop_fee, ' ', _r_phone)
            '''

            _writer.writerow((_r_ID, _r_pjname, _r_alias, _r_aoi, _r_x, _r_y, _add1, _add2, _r_dev, _r_tag,
                              _r_prop_compy, _r_prop_fee, _r_phone))

    except ValueError as e:
        raise e
    finally:
        pass


def write_csv(region, kw, n=3):
    _start = time.time()
    _num = 1
    for page in range(n):
        _get_project_list(region, kw, page)
        # 防止访问频率太高，避免被百度公司封
        time.sleep(1)
        if _num % 20 == 0:
            time.sleep(2)
        if _num % 100 == 0:
            time.sleep(3)
        if _num % 200 == 0:
            time.sleep(7)
        _num = _num + 1

    _end = time.time()
    _last_time = int((_end - _start))
    print('耗时' + str(_last_time) + 's')

'''
# test code
_get_project_list("631", "小区", 2)
'''

write_csv("631", "小区", 2)
