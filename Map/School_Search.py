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
from Map.Public import school


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
        f = open('/Users/liaoying/Desktop/Python Project/Baidu/dic/school', 'w')
        f.write(_r_list[0])
        f.close()
        '''

        for _r in _r_list:

            # find the id of school
            _pattern = r'(?<=primary_uid.:.).+?(?=")'
            _primary_uid = re.findall(_pattern, _r)
            _r_ID = _primary_uid[0]

            # find the school's name
            _pattern = r'(?<=\b"\},"name":").+?(?=")'
            _sch_name = re.findall(_pattern, _r)
            if not _sch_name:
                _pattern = r'(?<=\b,"name":").+?(?=")'
                _sch_name = re.findall(_pattern, _r)
            _r_sch_name = _sch_name[0]

            # find the alias of school
            _pattern = r'(?<=alias.:.).+?(?=])'
            _alias = re.findall(_pattern, _r)
            if not _alias:
                _r_alias = "Null"
            else:
                _r_alias = _alias[0]

            # find the address of school
            _pattern = r'(?<=poi_address.:.).+?(?=")'
            _address = re.findall(_pattern, _r)
            _add1 = _address[0]
            _pattern = r'.+?(?=")'
            adr = re.findall(_pattern, _r)
            _pattern = r'\(.+?\['
            _address = re.sub(_pattern, '', adr[0])
            _pattern = r'\(.+?\]'
            _add2 = re.sub(_pattern, '', _address)

            # find the coordinate(x,y) of school
            _pattern = r'(?<=navi_x.:.).+?(?=")'
            _navi_x = re.findall(_pattern, _r)
            if _navi_x:
                _r_x = _navi_x[0]
            else:
                _r_x = 0
            _pattern = r'(?<=navi_y.:.).+?(?=")'
            _navi_y = re.findall(_pattern, _r)
            if _navi_y:
                _r_y = _navi_y[0]
            else:
                _r_y = 0

            # find the tag of school
            _pattern = r'(?<=std_tag.:.).+?(?=")'
            _std_tag = re.findall(_pattern, _r)
            _r_tag = _std_tag[0]

            # find the plate of school
            _pattern = r'(?<=aoi.:.).+?(?=")'
            _aoi = re.findall(_pattern, _r)
            if _aoi:
                _r_aoi = _aoi[0]
                _r_aoi = re.sub(r'",', 'Null', _r_aoi)
            else:
                _r_aoi = 'Null'

            _school = school
            _school.ID = _r_ID
            _school.Name = _r_sch_name
            _school.Alias = _r_alias
            _school.Aoi = _r_aoi
            _school.Mct_x = _r_x
            _school.Mct_y = _r_y
            _school.Add1 = _add1
            _school.Add2 = _add2
            _school.Type = _r_tag

            print(_school.ID, ' ', _school.Name, ' ', _school.Alias, ' ', _school.Aoi, ' ', _school.Mct_x, ' '
                  , _school.Mct_y, ' ', _school.Add1, ' ', _school.Add2, ' ', _school.Type, ' ',
                  _school.pix_area_code)

    except ValueError as e:
        raise e
    finally:
        pass


_get_project_list("631", "小学", 2)