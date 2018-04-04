# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.02.26
Description:
- this file include some public function and class


"""

import re, xlwt, sqlite3, os, time

''' === define the sqlite list to tuple ==='''


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


''' === define the globe param ===='''


def parameter_search():
    _parameter = {
        """
        if the value of param is zero that means it's not used
        """
        "newmap": "1",  # don't know the usage
        "reqflag": "pcmap",  # don't know the usage
        "biz": "1",  # don't know the usage
        "from": "webmap",  # don't know the usage
        "da_par": "direct",  # don't know the usage
        "pcevaname": "pc4.1",  # don't know the usage
        "qt": "con",  # don't know the usage
        "c": "",  # the city code which defined by the baidu, 城市代码
        "wd": "",  # the keyword 搜索关键词
        "wd2": "",  # the keyword 搜索关键词
        "pn": "",  # the page's No 页数
        "nn": "",  # the total number of page
        "db": "0",  # don't know the usage
        "sug": "0",  # don't know the usage
        "addr": "0",  # the address
        # "da_src": "pcmappg.poi.page",
        # "on_gel": "1",
        # "src": "7",
        # "gr": "3",
        # "l": "12",
        # "tn": "B_NORMAL_MAP",
        # "u_loc": "12621219.536556,2630747.285024", # maybe the point of POI
        "ie": "utf-8",
        # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
        # "t": "1468896652886" # time
    }
    return _parameter


def _get_area_name(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __pattern = r'(?<=area_name.:.).+?(?=.,)'
    __area_name = re.findall(__pattern, __r)
    return __area_name[0]


def _get_area_code(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __pattern = r'(?<=area":).+?(?=,)'
    __area_code = re.findall(__pattern, __r)
    return __area_code[0]


def _get_id(r_split):
    """
    :usage: it's used for find the object's id
    :param r_split: the input is a list
    :return: ID, the object's id in the spider results
    """
    __r = r_split
    __pattern = r'(?<=primary_uid.:.).+?(?=")'
    __primary_uid = re.findall(__pattern, __r)
    __r_ID = __primary_uid[0]
    return __r_ID


def _get_name(r_split: str):
    """
    it's used for find the object's name,just like project_name, school_name,maybe different object has
    different rules
    :param r_split: the input is a list
    :return: Name, the object's name in the spider results
    """
    __r = r_split
    __pattern = r'(?<=\b"\},"name":").+?(?=")'
    __name = re.findall(__pattern, __r)
    if not __name:
        __pattern = r'(?<=\b,"name":").+?(?=")'
        __name = re.findall(__pattern, __r)
    __r_name = __name[0]
    return __r_name


def _get_alias(r_split: str):
    """
    it's used for find the object's even used name,It's a string.
    :param r_split: the input is a list
    :return: Name, the object's alias in the spider results
    """
    __r = r_split
    __pattern = r'(?<=alias.:.).+?(?=])'
    __alias = re.findall(__pattern, __r)
    if __alias:
        __r_alias = re.sub(r'"', "", __alias[0])
    else:
        __r_alias = None
    return __r_alias


def _get_plate(r_split: str):
    """
    it's used for find the object's plate, It's a user defined area, not in the map.
    :param r_split: the input is a list
    :return: Name, the object's plate in the spider results, its tag is aoi
    """
    __r = r_split
    __pattern = r'(?<=aoi.:.).+?(?=")'
    __aoi = re.findall(__pattern, __r)
    if __aoi:
        __r_aoi = __aoi[0]
        __r_aoi = re.sub(r'",', 'Null', __r_aoi)
    else:
        __r_aoi = None
    return __r_aoi


def _get_add1(r_split: str):
    """
    it's used for find the object's address,the add1 is a string that describe the current address of object
    :param r_split: the input is a list
    :return: Name, the object's add1 in the spider results
    """
    __r = r_split
    __pattern = r'(?<=poi_address.:.).+?(?=")'
    __address = re.findall(__pattern, __r)
    if __address:
        __add1 = __address[0]
    else:
        __add1 = None
    return __add1


def _get_add2(r_split: str):
    """
    it's used for find the object's address,the add1 is a string that describe the current address of object
    :param r_split: the input is a list
    :return: Name, the object's add1 in the spider results
    """
    __r = r_split
    __pattern = r'(?<="address_norm.:.).+?(?=",)'
    __adr = re.findall(__pattern, __r)
    if __adr:
        __pattern = r'\(.+?\['
        __address = re.sub(__pattern, '', __adr[0])
        __pattern = r'\(.+?\]'
        __address = re.sub(__pattern, '', __address)
        __pattern = r'\['
        __add2 = re.sub(__pattern, '', __address)
    else:
        __add2 = None
    return __add2


def _get_dev(r_split: str):
    """
    it's used for find the project's developer,maybe it's only used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's developer in the spider results
    """
    __r = r_split
    __pattern = r'(?<=developers.:.).+?(?=")'
    __developer = re.findall(__pattern, __r)
    if __developer:
        __r_dev = __developer[0]
    else:
        __r_dev = None
    return __r_dev


def _get_type(r_split: str):
    """
    it's used for find the project's type, actually, it's the different level
    :param r_split: the input is a list
    :return: Name, the object's type in the spider results
    """
    __r = r_split
    __pattern = r'(?<=std_tag.:.).+?(?=")'
    __std_tag = re.findall(__pattern, __r)
    if __std_tag:
        __r_tag = __std_tag[0]
    else:
        __r_tag = None
    return __r_tag


def _get_prop_company(r_split: str):
    """
    it's used for find the project's prosperity company, it's also used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's prosperity company in the spider results
    """
    __r = r_split
    __pattern = r'(?<=property_company.:.).+?(?=")'
    __property_company = re.findall(__pattern, __r)
    # _property_company = re.sub(r'",', "", _property_company)
    if __property_company:
        __r_prop_compy = __property_company[0]
        __r_prop_compy = re.sub(r'",', 'Null', __r_prop_compy)
    else:
        __r_prop_compy = None
    return __r_prop_compy


def _get_prop_fee(r_split: str):
    """
    it's used for find the project's prosperity fee, it's also used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's prosperity fee in the spider results
    """
    __r = r_split
    __pattern = r'(?<=property_management_fee.:.).+?(?=")'
    __property_management_fee = re.findall(__pattern, __r)
    # _property_management_fee = re.sub(r'",', "", _property_management_fee)
    if __property_management_fee:
        __r_prop_fee = __property_management_fee[0]
        __r_prop_fee = re.sub(r'",', 'Null', __r_prop_fee)
    else:
        __r_prop_fee = "0"
    return __r_prop_fee


def _get_phone(r_split: str):
    """
    it's used for find the object's phone, if you are interesting, you can define the rule to check weather the
    result is a real phone
    :param r_split: the input is a list
    :return: Name, the object's phone company in the spider results
    """
    __r = r_split
    __pattern = r'(?<="phone":").+?(?=")'
    __phone = re.findall(__pattern, __r)
    if __phone:
        __r_phone = __phone[0]
        __r_phone = re.sub(r'",', 'null', __r_phone)
    else:
        __r_phone = None
    return __r_phone


def _get_navi_x(r_split: str):
    """
    it's used for find the object's pix coordinate, it's means the x site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    __r = r_split
    __p1 = r'(?<=navi_x.:.).+?(?=")'
    __x1 = re.findall(__p1, __r)
    if len(__x1) == 0:
        __x1 = ['0']
    __p2 = r'(?<="x":).+?(?=,)'
    __x2 = re.findall(__p2, __r)
    __x2 = ['0' if __x == '"0"' else __x for __x in __x2]
    if len(__x2) == 0:
        __x2 = ['0']
    __p3 = r'(?<="geo":"1\|).+?(?=,)'
    __x3 = re.findall(__p3, __r)

    if float(__x2[0]) > 0:
        __r_x = __x2[0]
    elif __x3[0] and float(__x3[0]) > 0:
        __r_x = __x3[0]
    elif float(__x1[0]) > 0:
        __r_x = __x1[0]
    else:
        __r_x = 0.0
    return __r_x


def _get_navi_y(r_split: str):
    """
    it's used for find the object's pix coordinate, it's means the y site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    __r = r_split
    __p1 = r'(?<=navi_y.:.).+?(?=")'
    __y1 = re.findall(__p1, __r)
    if len(__y1) == 0:
        __y1 = ['0']
    __p2 = r'(?<="y":).+?(?=})'
    __y2 = re.findall(__p2, __r)
    __y2 = ['0' if __y == '"0"' else __y for __y in __y2]
    if len(__y2) == 0:
        __y2 = ['0']
    __p3 = r'(?<="geo":"1\|).+?(?=;)'
    __y3 = re.findall(__p3, __r)
    __y3 = re.split(r',', __y3[0])

    if float(__y2[0]) > 0:
        __r_y = __y2[0]
    elif __y3[1] and float(__y3[1]) > 0:
        __r_y = __y3[1]
    elif float(__y1[0]) > 0:
        __r_y = __y1[0]
    else:
        __r_y = 0.0
    return __r_y


def _get_base_updatetime(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="update_time.:.).+?(?=")'
    __time = re.findall(__p, __r)
    if __time:
        __time = re.split(r'\.', __time[-1])
        __time = __time[0]
        __time = time.localtime(int(__time))
        __time = time.strftime("%Y-%m-%d %H:%M:%S", __time)
    else:
        __time = '1900-00-00 00:00:00'
    return __time


def _get_point_updatetime(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="navi_update_time.:).+?(?=,)'
    __time = re.findall(__p, __r)
    if __time:
        __time = re.split(r'\.', __time[-1])
        __time = __time[0]
        __time = time.localtime(int(__time))
        __time = time.strftime("%Y-%m-%d %H:%M:%S", __time)
    else:
        __time = '1900-00-00 00:00:00'
    return __time


"""
# I'm test code : 成都市鼓楼小学: 11586260.2779   3568139.31197
_school = school_info('fid', 'name', 'alias', 'aoi', 'add1', 'add2', 'type')
_school.mct_x = 11586260.2779
_school.mct_y = 3568139.31197
print(_school.mct_x, _school.mct_y)
print(_school.pix_area_x, _school.pix_area_y)
"""

''' ====== format the unit in the xls.file ======='''


def _set_style(name, height, bold=False):
    """

    :param name:
    :param height:
    :param bold:
    :return:
    """
    __style = xlwt.XFStyle()  # 初始化样式

    __font = xlwt.Font()  # 为样式创建字体
    __font.name = name  # 'Times New Roman'
    __font.bold = bold
    __font.color_index = 4
    __font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    __style.font = __font
    # style.borders = borders

    return __style


''' ======= define the xls file write function ============='''

# school: ID, Name, Alias, plate, Add1, Add2, Type(Tag)，mct_x(lon), mct_y(lat), area_code_x, area_code_y
_school_row = [u'ID', u'学校名称', u'曾用名', u'版块', u'地址1', u'地址2', u'类别', u'像素X', u'像素y',
               u'地图区域码x', '地图区域码y']
_project_row = []


def _get_objects_id(t_name: str):
    """

    :param t_name: the object's name in the db
    :return: a list inclued objects' value of attribute
    """
    __t_name = t_name
    __dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
    __con = sqlite3.connect(__dir)
    __con.row_factory = _dict_factory
    __cur = __con.cursor()
    # the school_info use Bd_lng, the other use BD_lng
    __sql = ('select Id, Pix_X, Pix_Y FROM %s WHERE BD_lat IS NULL OR Bd_lng IS NULL' % __t_name)
    try:
        __cur.execute(__sql)
        __r = __cur.fetchall()
        __coordinate = []
        if __r:
            for __mct in __r:
                __pix = pix_coordinate_object(__mct)
                __coordinate.append(__pix)
        __cur.close()
        return __coordinate
    except ValueError as e:
        raise e
    finally:
        pass


def _write_bd09_sql(t_name: str, bd_coor):
    """

    :param t_name:
    :param bd_coor:
    :return:
    """
    __bd_coor = bd_coor
    __t_name = t_name
    # the school_info use Bd_lng, the other use BD_lng
    __search = "UPDATE %s SET BD_lat = ?, Bd_lng = ? WHERE Id = ?" % __t_name
    if __bd_coor.id:
        __dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
        __con = sqlite3.connect(__dir)
        __con.row_factory = _dict_factory
        __cur = __con.cursor()
        __cur.execute(__search, (__bd_coor.lat, __bd_coor.lng, __bd_coor.id))
        __con.commit()
        __con.close()
        print("\n%s 修改成功" % __bd_coor.id)
    else:
        print("\npublic._write_bd09_sql：无百度坐标数据修改！")


def _mall_hours(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<=shop_hours":").+?(?=",)'
    __hour = re.findall(__p, __r)
    if __hour:
        __h = __hour[0]
    else:
        __h = None
    return __h


def _mall_floor(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="bigdata":{).+?(?="})'
    __r = re.findall(__p, __r)
    __str1 = ''
    __str2 = ''
    if __r:
        __p = r'(?<=floor.:....).+?(?=.],)'
        __floor = re.findall(__p, __r[0])
        if __floor:
            __r = re.split(r'\|', __floor[0])
            if __r[0][0] == 'B':
                __str1 = '地下 %s 层 ' % __r[0][1]
            if __r[-1][0] == 'F':
                __str2 = '地上 %s 层' % __r[-1][1]
            __f = __str1 + __str2
        else:
            __f = None
    else:
        __f = None
    return __f


def _get_line_name(r_split: str):
    """
    It's used for getting line name
    :param r_split:
    :return __line_name:
    """
    __r = r_split
    __p = r'(?<="line_direction.:.).+?(?="nearest_station_idx)'
    __r = re.findall(__p, __r)
    __p = r'(?<=name.:.).+?(?=",)'
    __line = re.findall(__p, __r[0])
    if __line:
        __line_name = __line[0]
    else:
        __line_name = None
    return __line_name


def _get_line_price(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="maxPrice":).+?(?=,)'
    __r = re.findall(__p, __r)
    if __r:
        __max_price = __r[0]
    else:
        __max_price = 0
    return __max_price


def _get_line_time(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="timetable":.).+?(?=",)'
    __r = re.findall(__p, __r)
    if __r:
        __line_time = __r[0]
        __line_time = __line_time.strip()
    else:
        __line_time = None
    return __line_time


def _get_line_id(r_split: str):
    __r = r_split
    __p = r'(?<="timetable":.).+?(?="workTime")'
    __r = re.findall(__p, __r)
    __p = r'(?<="uid":.).+?(?=",)'
    __id = re.findall(__p, __r[0])
    if __r:
        __line_id = __id[0]
    else:
        __line_id = None
    return __line_id


def _get_line_color(r_split: str):
    __r = r_split
    __p = r'(?<="lineColor":.).+?(?="\})'
    __color = re.findall(__p, __r)
    if __color:
        __line_color = __color[0]
    else:
        __line_color = None
    return __line_color


def _get_station_pixx(r_split: str):
    """
    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="1\|).+?(?=,)'
    __coor = re.findall(__p, __r)
    if __coor:
        __pix_x = __coor[0]
    else:
        __pix_x = None
    return __pix_x


def _get_station_pixy(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="1).+?(?=;")'
    __coor = re.findall(__p, __r)
    if __coor:
        __p = r'(?<=,).+?(?=;)'
        __y = re.findall(__p, __coor[0])
        __pix_y = __y[0]
    else:
        __pix_y = None
    return __pix_y


def _get_station_name(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="name":.).+?(?=.,"operation_times)'
    __name = re.findall(__p, __r)
    __st_name = __name[0]
    return __st_name


def _get_station_endtime(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="end_time":.).+?(?=",)'
    __time = re.findall(__p, __r)
    __end_time = __time[0]
    return __end_time


def _get_station_starttime(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="start_time":.).+?(?="})'
    __time = re.findall(__p, __r)
    __start_time = __time[0]
    return __start_time


def _get_station_subway(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<=fff">).+?(?=<)'
    __st_sub = re.findall(__p, __r)
    if __st_sub:
        __subway = __st_sub[0]
    else:
        __subway = None
    return __subway


def _get_station_transfer(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="transfer":\[\[).+?(?=\]\],)'
    __st_tran = re.findall(__p, __r)
    if __st_tran:
        __transfer = __st_tran[0]
    else:
        __transfer = None
    return __transfer


def _get_station_id(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p = r'(?<="uid":").+?(?=")'
    __st_id = re.findall(__p, __r)
    if __st_id:
        __Id = __st_id[-1]
    else:
        __Id = None
    return __Id


def _get_cla_id(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p1 = r'(?<="cla":.).+?(?=\],"click_flag")'
    __c = re.findall(__p1, __r)
    if __c:
        __p2 = r'(?<=\],\[).+?(?=\])'
        __c2 = re.findall(__p2, __c[0])
        if __c2:
            __cla = __c2[0]
        else:
            __cla = None
    else:
        __cla = None
    return __cla


def _get_std_id(r_split: str):
    """

    :param r_split:
    :return:
    """
    __r = r_split
    __p1 = r'(?<="std_tag_id.:.).+?(?=",)'
    __c = re.findall(__p1, __r)
    if __c:
        __std_tag_id = __c[0]
    else:
        __std_tag_id = None
    return __std_tag_id


def _get_prj_uid(r_split: str):
    __r = r_split
    __p1 = r'(?<="street_id.:.).+?(?=",)'
    __c = re.findall(__p1, __r)
    if __c:
        __prj_uid = __c[0]
    else:
        __prj_uid = None
    return __prj_uid


''' ================= define the class of mct_point ================='''


class mct_point():
    """
    -   usage: format mct_point and the area code in the Baidu Map,
        this is the public class used for the all object
    -   attribute: mct_x(lon), mct_y(lat), area_code_x, area_code_y
    """

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def mct_x(self):
        _mct_x = float(_get_navi_x(self._r_split))
        return _mct_x

    @property
    def mct_y(self):
        _mct_y = float(_get_navi_y(self._r_split))
        return _mct_y

    @property
    def pix_area_x(self):
        _pix_area_x = int(self.mct_x / 250)
        return _pix_area_x

    @property
    def pix_area_y(self):
        _pix_area_y = int(self.mct_y / 250)
        return _pix_area_y


''' ================== define the class of school_base() ==================='''


class school_base():
    """
    -   usage: format the the base info of school
    -   attribute: ID, Name, Alias, plate, Add1, Add2, Type(Tag)
    """

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def id(self):
        _id = _get_id(self._r_split)
        return _id

    @property
    def name(self):
        _name = _get_name(self._r_split)
        return _name

    @property
    def alias(self):
        _alias = _get_alias(self._r_split)
        return _alias

    @property
    def plate(self):
        _plate = _get_plate(self._r_split)
        return _plate

    @property
    def add1(self):
        _add1 = _get_add1(self._r_split)
        return _add1

    @property
    def add2(self):
        _add2 = _get_add2(self._r_split)
        return _add2

    @property
    def cla(self):
        _cla = _get_cla_id(self._r_split)
        return _cla

    @property
    def type(self):
        _type = _get_type(self._r_split)
        return _type

    @property
    def std_id(self):
        _std_id = _get_std_id(self._r_split)
        return _std_id

    @property
    def area_name(self):
        _area_name = _get_area_name(self._r_split)
        return _area_name

    @property
    def area_code(self):
        _area_code = _get_area_code(self._r_split)
        return _area_code

    @property
    def base_update_time(self):
        _base_update_time = _get_base_updatetime(self._r_split)
        return _base_update_time

    @property
    def point_update_time(self):
        _point_update_time = _get_point_updatetime(self._r_split)
        return _point_update_time


class school_info(school_base, mct_point):
    pass


''' ======================== define the class of project_base ==========================='''


class proj_base():
    """
    -   usage: format the base info of community
    -   attribute: ID, pj_name, alias, aoi, _add1, _add2, dev, tag, prop_company, prop_fee
    """

    def __index__(self, r_split):
        self._r_split = r_split

    @property
    def id(self):
        __id = _get_id(self._r_split)
        return __id

    @property
    def name(self):
        __name = _get_name(self._r_split)
        return __name

    @property
    def alias(self):
        __alias = _get_alias(self._r_split)
        return __alias

    @property
    def plate(self):
        __plate = _get_plate(self._r_split)
        return __plate

    @property
    def add1(self):
        __add1 = _get_add1(self._r_split)
        return __add1

    @property
    def add2(self):
        __add2 = _get_add2(self._r_split)
        return __add2

    @property
    def type(self):
        __type = _get_type(self._r_split)
        return __type

    @property
    def developer(self):
        __dev = _get_dev(self._r_split)
        return __dev

    @property
    def prop_company(self):
        __prop_name = _get_prop_company(self._r_split)
        return __prop_name

    @property
    def prop_fee(self):
        __fee = _get_prop_fee(self._r_split)
        return __fee

    @property
    def street_id(self):
        __st_id = _get_prj_uid(self._r_split)
        return __st_id

    @property
    def base_update_time(self):
        __base_update_time = _get_base_updatetime(self._r_split)
        return __base_update_time

    @property
    def point_update_time(self):
        __point_update_time = _get_point_updatetime(self._r_split)
        return __point_update_time

    @property
    def area_name(self):
        __area_name = _get_area_name(self._r_split)
        return __area_name

    @property
    def area_code(self):
        __area_code = _get_area_code(self._r_split)
        return __area_code


class proj_info(proj_base, mct_point):
    pass


''' ================== define the class of hospital ==================='''


class hosptial_base():
    """
    -   usage: format the the base info of hospital
    -   attribute: ID, Name, plate, Add1, Add2, Type(Tag), Area_Name, Area_Code, base_update_time, point_update_time
    """

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def id(self):
        _id = _get_id(self._r_split)
        return _id

    @property
    def name(self):
        _name = _get_name(self._r_split)
        return _name

    @property
    def plate(self):
        _plate = _get_plate(self._r_split)
        return _plate

    @property
    def add1(self):
        _add1 = _get_add1(self._r_split)
        return _add1

    @property
    def add2(self):
        _add2 = _get_add2(self._r_split)
        return _add2

    @property
    def type(self):
        _type = _get_type(self._r_split)
        return _type

    @property
    def area_name(self):
        _area_name = _get_area_name(self._r_split)
        return _area_name

    @property
    def area_code(self):
        _area_code = _get_area_code(self._r_split)
        return _area_code

    @property
    def base_update_time(self):
        _base_update_time = _get_base_updatetime(self._r_split)
        return _base_update_time

    @property
    def point_update_time(self):
        _point_update_time = _get_point_updatetime(self._r_split)
        return _point_update_time


class hospital_info(hosptial_base, mct_point):
    pass


''' ================== define the class of coordinate ==================='''


class pix_coordinate_object():
    """
    It's used for the pix coordinate's instantiation
    """

    def __init__(self, pix_c: dict):
        self.__pix_coordinate = pix_c

    @property
    def id(self):
        id = self.__pix_coordinate["Id"]
        return id

    @property
    def pix_x(self):
        pix_x = str(self.__pix_coordinate["Pix_X"])
        return pix_x

    @property
    def pix_y(self):
        pix_y = str(self.__pix_coordinate["Pix_Y"])
        return pix_y


class bd09_coordinate_object():
    """
    It's used for the bd09 coordinate's instantiation
    """

    def __init__(self, Id, lat, lng, address):
        self.id = Id
        self.lat = float(lat)  # get 纬度
        self.lng = float(lng)  # get 经度
        self.address = address

    pass


''' ================== define the class of mall ==================='''


class mall_base():
    """
    -   usage: format the the base info of Mall
    -   attribute: ID, Name, plate, Add1, Add2, Type(Tag), Area_Name, Area_Code, Shop_Hours, Floor
        base_update_time, point_update_time,
    """

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def id(self):
        __id = _get_id(self._r_split)
        return __id

    @property
    def name(self):
        __name = _get_name(self._r_split)
        return __name

    @property
    def plate(self):
        _plate = _get_plate(self._r_split)
        return _plate

    @property
    def add1(self):
        __add1 = _get_add1(self.r_split)
        return __add1

    @property
    def add2(self):
        __add2 = _get_add2(self._r_split)
        return __add2

    @property
    def type(self):
        __type = _get_type(self._r_split)
        return __type

    @property
    def area_name(self):
        __area_name = _get_area_name(self._r_split)
        return __area_name

    @property
    def area_code(self):
        __area_code = _get_area_code(self._r_split)
        return __area_code

    @property
    def base_update_time(self):
        __base_update_time = _get_base_updatetime(self._r_split)
        return __base_update_time

    @property
    def point_update_time(self):
        __point_update_time = _get_point_updatetime(self._r_split)
        return __point_update_time

    @property
    def mall_hours(self):
        __shop_hours = _mall_hours(self._r_split)
        return __shop_hours

    @property
    def mall_floor(self):
        __mall_floor = _mall_floor(self._r_split)
        return __mall_floor


class mall_info(mall_base, mct_point):
    pass


''' === define the class of metro line information ===='''


class matro_line_info():

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def line_id(self):
        __line_id = _get_line_id(self._r_split)
        return __line_id

    @property
    def line_name(self):
        __line_name = _get_line_name(self._r_split)
        return __line_name

    @property
    def line_time(self):
        __line_time = _get_line_time(self._r_split)
        return __line_time

    @property
    def max_price(self):
        __max_price = _get_line_price(self._r_split)
        return __max_price

    @property
    def line_color(self):
        __line_color = _get_line_color(self._r_split)
        return __line_color

    @property
    def creat_date(self):
        __creat_date = time.strftime("%Y-%m-%d")
        return __creat_date


''' === define the class of station information ===='''


class station_info():

    def __init__(self, r_split, line_id):
        self._r_split = r_split
        self.line_id = line_id

    @property
    def st_id(self):
        __Id = _get_station_id(self._r_split)
        return __Id

    @property
    def st_name(self):
        __st_name = _get_station_name(self._r_split)
        return __st_name

    @property
    def st_start_time(self):
        __start_time = _get_station_starttime(self._r_split)
        return __start_time

    @property
    def st_end_time(self):
        __end_time = _get_station_endtime(self._r_split)
        return __end_time

    @property
    def st_subway(self):
        __subway = _get_station_subway(self._r_split)
        return __subway

    @property
    def st_transfer(self):
        __transfer = _get_station_transfer(self._r_split)
        return __transfer

    @property
    def st_pix_x(self):
        __pix_x = _get_station_pixx(self._r_split)
        return __pix_x

    @property
    def st_pix_y(self):
        __pix_y = _get_station_pixy(self._r_split)
        return __pix_y

    @property
    def creat_date(self):
        __creat_date = time.strftime("%Y-%m-%d")
        return __creat_date


''' === define the class of park information ===='''


class park_base():

    def __init__(self, r_split):
        self._r_split = r_split

    @property
    def park_id(self):
        __park_id = _get_id(self._r_split)
        return __park_id

    @property
    def park_name(self):
        __park_name = _get_name(self._r_split)
        return __park_name

    @property
    def park_alias(self):
        __park_alias = _get_alias(self._r_split)
        return __park_alias

    @property
    def park_add1(self):
        __park_addr = _get_add1(self._r_split)
        return __park_addr

    @property
    def park_add2(self):
        __park_addr = _get_add2(self._r_split)
        return __park_addr

    @property
    def park_area_code(self):
        __park_area_code = _get_area_code(self._r_split)
        return __park_area_code

    @property
    def park_area_name(self):
        __park_area_name = _get_area_name(self._r_split)
        return __park_area_name

    @property
    def park_plate(self):
        __park_plate = _get_plate(self._r_split)
        return __park_plate

    @property
    def park_cla_id(self):
        __cla_id = _get_cla_id(self._r_split)
        return __cla_id

    @property
    def park_std_tag(self):
        __park_std_tag = _get_type(self._r_split)
        return __park_std_tag

    @property
    def park_std_id(self):
        __park_std_id = _get_std_id(self._r_split)
        return __park_std_id

    @property
    def info_update_date(self):
        __info_update_date = _get_base_updatetime(self._r_split)
        return __info_update_date

    @property
    def point_update_date(self):
        __point_update_date = _get_point_updatetime(self._r_split)
        return __point_update_date


class park_info(park_base, mct_point):
    pass