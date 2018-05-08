"""

Author: Wayne
Ver: v0.0.1
Date: 2018.05.04
Description:
- this module is using for define some objects' class

"""


class connection:

    @property
    def geo_key(self):
        __key = '6a7e8136679e01f9ac129e01fbb1fb06'
        return __key

    @property
    def geo_url(self):
        __url = 'http://restapi.amap.com/v3/geocode/geo'
        return __url


class proj:

    def __init__(self, r_split: dict):
        self.__r_split = r_split

    @property
    def address(self):
        __addr = self.__r_split["formatted_address"]
        return __addr

    @property
    def province(self):
        __province = self.__r_split["province"]
        return __province

    @property
    def district(self):
        __district = self.__r_split["district"]
        return __district

    @property
    def adcode(self):
        __adcode = self.__r_split["adcode"]
        return __adcode

    @property
    def street(self):
        __street = self.__r_split["street"] + self.__r_split["number"]
        return __street

    @property
    def location(self):
        __location = self.__r_split["location"]
        return __location


class or_proj:

    def __init__(self, oracle_proj: dict):
        self.__r = oracle_proj
    # id, PROJECT_NAME, GD_NAME, LJ_NAME, DISTRICT_ADD, REGION, ADD_LNG, ADD_LAT, SYS_UPDATE_TIME

    @property
    def r_id(self):
        __r_id = self.__r["ID"]
        return __r_id

    @property
    def pj_name(self):
        __r_pj_name = self.__r["PROJECT_NAME"]
        return __r_pj_name

    @property
    def gd_name(self):
        __r_gd_name = self.__r["GD_NAME"]
        return __r_gd_name

    @property
    def lj_name(self):
        __r_lj_name = self.__r["LJ_NAME"]
        return __r_lj_name

    @property
    def ds_addr(self):
        __r_ds_addr = self.__r["DISTRICT_ADD"]
        return __r_ds_addr

    @property
    def region(self):
        __r_region = self.__r["REGION"]
        return __r_region

    @property
    def addr_lng(self):
        __r_addr_lng = self.__r["ADD_LNG"]
        return __r_addr_lng

    @property
    def addr_lat(self):
        __r_addr_lat = self.__r["ADD_LAT"]
        return __r_addr_lat

    @property
    def name_lng(self):
        __r_name_lng = self.__r["NAME_LNG"]
        return __r_name_lng

    @property
    def name_lat(self):
        __r_name_lat = self.__r["NAME_LAT"]
        return __r_name_lat