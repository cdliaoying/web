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
    _r = r_split
    _pattern = r'(?<=area_name.:.).+?(?=.,)'
    _area_name = re.findall(_pattern, _r)
    return _area_name[0]


def _get_area_code(r_split: str):
    """

    :param r_split:
    :return:
    """
    _r = r_split
    _pattern = r'(?<=area":).+?(?=,)'
    _area_code = re.findall(_pattern, _r)
    return _area_code[0]


def _get_id(r_split):
    """
    :usage: it's used for find the object's id
    :param r_split: the input is a list
    :return: ID, the object's id in the spider results
    """
    _r = r_split
    _pattern = r'(?<=primary_uid.:.).+?(?=")'
    _primary_uid = re.findall(_pattern, _r)
    _r_ID = _primary_uid[0]
    return _r_ID


def _get_name(r_split: str):
    """
    it's used for find the object's name,just like project_name, school_name,maybe different object has
    different rules
    :param r_split: the input is a list
    :return: Name, the object's name in the spider results
    """
    _r = r_split
    _pattern = r'(?<=\b"\},"name":").+?(?=")'
    _name = re.findall(_pattern, _r)
    if not _name:
        _pattern = r'(?<=\b,"name":").+?(?=")'
        _name = re.findall(_pattern, _r)
    _r_name = _name[0]
    return _r_name


def _get_alias(r_split: str):
    """
    it's used for find the object's even used name,It's a string.
    :param r_split: the input is a list
    :return: Name, the object's alias in the spider results
    """
    _r = r_split
    _pattern = r'(?<=alias.:.).+?(?=])'
    _alias = re.findall(_pattern, _r)
    if _alias:
        _r_alias = re.sub(r'"', "", _alias[0])
    else:
        _r_alias = "Null"
    return _r_alias


def _get_plate(r_split: str):
    """
    it's used for find the object's plate, It's a user defined area, not in the map.
    :param r_split: the input is a list
    :return: Name, the object's plate in the spider results, its tag is aoi
    """
    _r = r_split
    _pattern = r'(?<=aoi.:.).+?(?=")'
    _aoi = re.findall(_pattern, _r)
    if _aoi:
        _r_aoi = _aoi[0]
        _r_aoi = re.sub(r'",', 'Null', _r_aoi)
    else:
        _r_aoi = 'Null'
    return _r_aoi


def _get_add1(r_split: str):
    """
    it's used for find the object's address,the add1 is a string that describe the current address of object
    :param r_split: the input is a list
    :return: Name, the object's add1 in the spider results
    """
    _r = r_split
    _pattern = r'(?<=poi_address.:.).+?(?=")'
    _address = re.findall(_pattern, _r)
    if _address:
        _add1 = _address[0]
    else:
        _add1 = 'Null'
    return _add1


def _get_add2(r_split: str):
    """
    it's used for find the object's address,the add1 is a string that describe the current address of object
    :param r_split: the input is a list
    :return: Name, the object's add1 in the spider results
    """
    _r = r_split
    _pattern = r'(?<="address_norm.:.).+?(?=",)'
    adr = re.findall(_pattern, _r)
    if adr:
        _pattern = r'\(.+?\['
        _address = re.sub(_pattern, '', adr[0])
        _pattern = r'\(.+?\]'
        _address = re.sub(_pattern, '', _address)
        _pattern = r'\['
        _add2 = re.sub(_pattern, '', _address)
    else:
        _add2 = 'Null'
    return _add2


def _get_dev(r_split: str):
    """
    it's used for find the project's developer,maybe it's only used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's developer in the spider results
    """
    _r = r_split
    _pattern = r'(?<=developers.:.).+?(?=")'
    _developer = re.findall(_pattern, _r)
    if _developer:
        _r_dev = _developer[0]
    else:
        _r_dev = "Null"
    return _r_dev


def _get_type(r_split: str):
    """
    it's used for find the project's type, actually, it's the different level
    :param r_split: the input is a list
    :return: Name, the object's type in the spider results
    """
    _r = r_split
    _pattern = r'(?<=std_tag.:.).+?(?=")'
    _std_tag = re.findall(_pattern, _r)
    if _std_tag:
        _r_tag = _std_tag[0]
    else:
        _r_tag = "Null"
    return _r_tag


def _get_prop_company(r_split: str):
    """
    it's used for find the project's prosperity company, it's also used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's prosperity company in the spider results
    """
    _r = r_split
    _pattern = r'(?<=property_company.:.).+?(?=")'
    _property_company = re.findall(_pattern, _r)
    # _property_company = re.sub(r'",', "", _property_company)
    if _property_company:
        _r_prop_compy = _property_company[0]
        _r_prop_compy = re.sub(r'",', 'Null', _r_prop_compy)
    else:
        _r_prop_compy = "Null"
    return _r_prop_compy


def _get_prop_fee(r_split: str):
    """
    it's used for find the project's prosperity fee, it's also used for the real estate
    :param r_split: the input is a list
    :return: Name, the object's prosperity fee in the spider results
    """
    _r = r_split
    _pattern = r'(?<=property_management_fee.:.).+?(?=")'
    _property_management_fee = re.findall(_pattern, _r)
    # _property_management_fee = re.sub(r'",', "", _property_management_fee)
    if _property_management_fee:
        _r_prop_fee = _property_management_fee[0]
        _r_prop_fee = re.sub(r'",', 'Null', _r_prop_fee)
    else:
        _r_prop_fee = "0"
    return _r_prop_fee


def _get_phone(r_split: str):
    """
    it's used for find the object's phone, if you are interesting, you can define the rule to check weather the
    result is a real phone
    :param r_split: the input is a list
    :return: Name, the object's phone company in the spider results
    """
    _r = r_split
    _pattern = r'(?<="phone":").+?(?=")'
    _phone = re.findall(_pattern, _r)
    if _phone:
        _r_phone = _phone[0]
        _r_phone = re.sub(r'",', 'null', _r_phone)
    else:
        _r_phone = "Null"
    return _r_phone


def _get_navi_x(r_split: str):
    """
    it's used for find the object's pix coordinate, it's means the x site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    _r = r_split
    _p1 = r'(?<=navi_x.:.).+?(?=")'
    _x1 = re.findall(_p1, _r)
    if len(_x1) == 0:
        _x1 = ['0']
    _p2 = r'(?<="x":).+?(?=,)'
    _x2 = re.findall(_p2, _r)
    _x2 = ['0' if x == '"0"' else x for x in _x2]
    if len(_x2) == 0:
        _x2 = ['0']
    _p3 = r'(?<="geo":"1\|).+?(?=,)'
    _x3 = re.findall(_p3, _r)

    if float(_x2[0]) > 0:
        _r_x = _x2[0]
    elif _x3[0] and float(_x3[0]) > 0:
        _r_x = _x3[0]
    elif float(_x1[0]) > 0:
        _r_x = _x1[0]
    else:
        _r_x = 0.0
    return _r_x


def _get_navi_y(r_split: str):
    """
    it's used for find the object's pix coordinate, it's means the y site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    _r = r_split
    _p1 = r'(?<=navi_y.:.).+?(?=")'
    _y1 = re.findall(_p1, _r)
    if len(_y1) == 0:
        _y1 = ['0']
    _p2 = r'(?<="y":).+?(?=})'
    _y2 = re.findall(_p2, _r)
    _y2 = ['0' if _y == '"0"' else _y for _y in _y2]
    if len(_y2) == 0:
        _y2 = ['0']
    _p3 = r'(?<="geo":"1\|).+?(?=;)'
    _y3 = re.findall(_p3, _r)
    _y3 = re.split(r',', _y3[0])

    if float(_y2[0]) > 0:
        _r_y = _y2[0]
    elif _y3[1] and float(_y3[1]) > 0:
        _r_y = _y3[1]
    elif float(_y1[0]) > 0:
        _r_y = _y1[0]
    else:
        _r_y = 0.0
    return _r_y


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
    _style = xlwt.XFStyle()  # 初始化样式

    _font = xlwt.Font()  # 为样式创建字体
    _font.name = name  # 'Times New Roman'
    _font.bold = bold
    _font.color_index = 4
    _font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    _style.font = _font
    # style.borders = borders

    return _style


''' ======= define the xls file write function ============='''

# school: ID, Name, Alias, plate, Add1, Add2, Type(Tag)，mct_x(lon), mct_y(lat), area_code_x, area_code_y
_school_row = [u'ID', u'学校名称', u'曾用名', u'版块', u'地址1', u'地址2', u'类别', u'像素X', u'像素y',
               u'地图区域码x', '地图区域码y']
_project_row = []


def school_write_sql(school_info):
    """
    the function is used for insert the school info into the db
    :param school_info: is class from the school_info
    :return: No return
    @:type school_info: class
    """
    _school = school_info
    _dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
    _con = sqlite3.connect(_dir)
    _con.row_factory = _dict_factory
    _cur = _con.cursor()
    try:
        _cur.execute("SELECT count(Id) AS num FROM school_info WHERE Id = ?", (_school.id,))
        _r = _cur.fetchall()
        if _r[0]["num"] == 0:
            _cur.execute("INSERT INTO school_info "
                         # "(Id, Name, Alias, Plate, Address, Address2, Type, Pix_X, Pix_Y, Area_X, Area_Y) "
                         "VALUES(?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                         (_school.id, _school.name, _school.alias, _school.plate, _school.add1,
                          _school.add2, _school.type, _school.mct_x, _school.mct_y, _school.pix_area_x,
                          _school.pix_area_y, _school.area_code, _school.area_name, _school.base_update_time,
                          _school.point_update_time))
            _con.commit()
        else:
            print("%s, %s 已存在!" % (_school.id, _school.name))
        _con.close()
    except ValueError as e:
        raise e
    finally:
        pass


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
    __sql = ('select Id, Pix_X, Pix_Y FROM %s WHERE BD_lat IS NULL OR BD_lng IS NULL' % __t_name)
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
    __bd_coor = bd_coor
    __t_name = t_name
    __search = "UPDATE %s SET BD_lat = ?, BD_lng = ? WHERE Id = ?" % __t_name
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
        __h = 'Null'
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
            __f = 'Null'
    else:
        __f = 'Null'
    return __f


''' ================= define the class of mct_point ================='''


class mct_point():
    """
    -   usage: format mct_point and the area code in the Baidu Map,
        this is the public class used for the all object
    -   attribute: mct_x(lon), mct_y(lat), area_code_x, area_code_y
    """

    def __init__(self, r_split):
        self.r_split = r_split

    @property
    def mct_x(self):
        _mct_x = float(_get_navi_x(self.r_split))
        return _mct_x

    @property
    def mct_y(self):
        _mct_y = float(_get_navi_y(self.r_split))
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
        self.r_split = r_split

    @property
    def id(self):
        _id = _get_id(self.r_split)
        return _id

    @property
    def name(self):
        _name = _get_name(self.r_split)
        return _name

    @property
    def alias(self):
        _alias = _get_alias(self.r_split)
        return _alias

    @property
    def plate(self):
        _plate = _get_plate(self.r_split)
        return _plate

    @property
    def add1(self):
        _add1 = _get_add1(self.r_split)
        return _add1

    @property
    def add2(self):
        _add2 = _get_add2(self.r_split)
        return _add2

    @property
    def type(self):
        _type = _get_type(self.r_split)
        return _type

    @property
    def area_name(self):
        _area_name = _get_area_name(self.r_split)
        return _area_name

    @property
    def area_code(self):
        _area_code = _get_area_code(self.r_split)
        return _area_code

    @property
    def base_update_time(self):
        _base_update_time = _get_base_updatetime(self.r_split)
        return _base_update_time

    @property
    def point_update_time(self):
        _point_update_time = _get_point_updatetime(self.r_split)
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
        self.r_split = r_split

    @property
    def id(self):
        _id = _get_id(self.r_split)
        return _id

    @property
    def name(self):
        _name = _get_name(self.r_split)
        return _name

    @property
    def alias(self):
        _alias = _get_alias(self.r_split)
        return _alias

    @property
    def plate(self):
        _plate = _get_plate(self.r_split)
        return _plate

    @property
    def add1(self):
        _add1 = _get_add1(self.r_split)
        return _add1

    @property
    def add2(self):
        _add2 = _get_add2(self.r_split)
        return _add2

    @property
    def type(self):
        _type = _get_type(self.r_split)
        return _type

    @property
    def developer(self):
        _dev = _get_dev(self.r_split)
        return _dev

    @property
    def prop_company(self):
        _prop_name = _get_prop_company(self.r_split)
        return _prop_name

    @property
    def prop_fee(self):
        _fee = _get_prop_fee(self.r_split)
        return _fee


class proj_info(proj_base, mct_point):
    pass


''' ================== define the class of hospital ==================='''


class hosptial_base():
    """
    -   usage: format the the base info of hospital
    -   attribute: ID, Name, plate, Add1, Add2, Type(Tag), Area_Name, Area_Code, base_update_time, point_update_time
    """

    def __init__(self, r_split):
        self.r_split = r_split

    @property
    def id(self):
        _id = _get_id(self.r_split)
        return _id

    @property
    def name(self):
        _name = _get_name(self.r_split)
        return _name

    @property
    def plate(self):
        _plate = _get_plate(self.r_split)
        return _plate

    @property
    def add1(self):
        _add1 = _get_add1(self.r_split)
        return _add1

    @property
    def add2(self):
        _add2 = _get_add2(self.r_split)
        return _add2

    @property
    def type(self):
        _type = _get_type(self.r_split)
        return _type

    @property
    def area_name(self):
        _area_name = _get_area_name(self.r_split)
        return _area_name

    @property
    def area_code(self):
        _area_code = _get_area_code(self.r_split)
        return _area_code

    @property
    def base_update_time(self):
        _base_update_time = _get_base_updatetime(self.r_split)
        return _base_update_time

    @property
    def point_update_time(self):
        _point_update_time = _get_point_updatetime(self.r_split)
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
        self.r_split = r_split

    @property
    def id(self):
        __id = _get_id(self.r_split)
        return __id

    @property
    def name(self):
        __name = _get_name(self.r_split)
        return __name

    @property
    def plate(self):
        _plate = _get_plate(self.r_split)
        return _plate

    @property
    def add1(self):
        __add1 = _get_add1(self.r_split)
        return __add1

    @property
    def add2(self):
        __add2 = _get_add2(self.r_split)
        return __add2

    @property
    def type(self):
        __type = _get_type(self.r_split)
        return __type

    @property
    def area_name(self):
        __area_name = _get_area_name(self.r_split)
        return __area_name

    @property
    def area_code(self):
        __area_code = _get_area_code(self.r_split)
        return __area_code

    @property
    def base_update_time(self):
        __base_update_time = _get_base_updatetime(self.r_split)
        return __base_update_time

    @property
    def point_update_time(self):
        __point_update_time = _get_point_updatetime(self.r_split)
        return __point_update_time

    @property
    def mall_hours(self):
        __shop_hours = _mall_hours(self.r_split)
        return __shop_hours

    @property
    def mall_floor(self):
        __mall_floor = _mall_floor(self.r_split)
        return __mall_floor


class mall_info(mall_base, mct_point):
    pass
