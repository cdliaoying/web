# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.02.26
Description:
- this file include some public function and class


"""

import re, xlwt, sqlite3, os


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


class school_info(school_base, mct_point):
    pass


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


def _get_name(r_split):
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


def _get_alias(r_split):
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


def _get_plate(r_split):
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


def _get_add1(r_split):
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


def _get_add2(r_split):
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


def _get_dev(r_split):
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


def _get_type(r_split):
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


def _get_prop_company(r_split):
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


def _get_prop_fee(r_split):
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


def _get_phone(r_split):
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


def _get_navi_x(r_split):
    """
    it's used for find the object's pix coordinate, it's means the x site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    _r = r_split
    _p1 = r'(?<=navi_x.:.).+?(?=")'
    _x1 = re.findall(_p1, _r)
    _p2 = r'(?<=x.:).+?(?=,)'
    _x2 = re.findall(_p2, _r)
    _x2 = _x2[0].replace('\"', '')
    _p3 = r'(?<="geo":"1).+?(?=,)'
    _x3 = re.findall(_p3, _r)
    _x3 = _x3[0].replace("|", "")

    if _x1:
        if float(_x1[0]) > 0:
            _r_x = _x1[0]
        else:
            if float(_x2) > 0:
                _r_x = _x2
            else:
                if float(_x3) > 0:
                    _r_x = _x3
                else:
                    _r_x = 0.0
    else:
        _r_x = 0.0
    return _r_x


def _get_navi_y(r_split):
    """
    it's used for find the object's pix coordinate, it's means the y site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    _r = r_split
    _pattern = r'(?<=navi_y.:.).+?(?=")'
    _navi_y = re.findall(_pattern, _r)
    if _navi_y:
        if float(_navi_y[0]) > 0:
            _r_y = _navi_y[0]
        else:
            _pattern = r'(?<=y.:).+?(?=,)'
            _navi_y = re.findall(_pattern, _r)
            print("\n navi_y: %s " % _navi_y[0])
            _navi_y = _navi_y[0].replace('\"', '')

            if float(_navi_y[0]) > 0:
                _r_y = _navi_y[0]
            else:
                _r = _r.replace("|", "")
                _pattern = r'(?<="geo":"1).+?(?=,)'
                _navi_y = re.findall(_pattern, _r)
                _navi_y = re.split(r',', _navi_y[0])
                _r_y = _navi_y[1]
    else:
        _r_y = 0.0
    return _r_y


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


'''
def school_write_excel(row0):
    """

    :return:
    """
    _f = xlwt.Workbook()  # 创建工作簿

    # create the first sheet : sheet1
    _sheet1 = _f.add_sheet(u'sheet1', cell_overwrite_ok=True)

    _row0 = row0
    #  column0 = [u'机票', u'船票', u'火车票', u'汽车票', u'其它']
    #  status = [u'预订', u'出票', u'退票', u'业务小计']

    # 生成第一行
    for i in range(0, len(row0)):
        _sheet1.write(0, i, row0[i], _set_style('Times New Roman', 220, True))

    _f.save('demo1.xlsx')  # 保存文件
'''


def school_write_sql(school_info):
    """
    the function is used for insert the school info into the db
    :param school_info: is class from the school_info
    :return: No return
    """
    _school = school_info
    _dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
    _con = sqlite3.connect(_dir)
    _con.row_factory = _dict_factory
    _cur = _con.cursor()
    try:
        _cur.execute("select count(Id) as num FROM school_info WHERE Id = ?", (_school.id, ))
        _r = _cur.fetchall()
        if _r[0]["num"] == 0:
            _cur.execute("INSERT INTO school_info "
                         # "(Id, Name, Alias, Plate, Address, Address2, Type, Pix_X, Pix_Y, Area_X, Area_Y) "
                         "VALUES(?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                         (_school.id, _school.name, _school.alias, _school.plate, _school.add1,
                         _school.add2, _school.type, _school.mct_x, _school.mct_y, _school.pix_area_x,
                         _school.pix_area_y))
            _con.commit()
        else:
            print("%s, %s 已存在!" % (_school.id, _school.name))
        _con.close()
    except ValueError as e:
        raise e
    finally:
        pass

