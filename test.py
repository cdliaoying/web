# -*- coding: utf-8 -*-
import re, os
from datetime import datetime

r = ['[四川省(32)|PROV|0|NONE][成都市(75)|CITY|0|NONE][青羊区(631)|AREA|1|NONE][金阳路()|ROAD|1|NONE]390号",'
     '"alias":["成都印象金沙","印象金沙小区"],"area":631,"area_name":"成都市青羊区",'
     '"biz_type":0,"brand_id":null,"catalogID":25,"cla":[[25,"地产小区"]],'
     '"click_flag":0,"detail":1,"diPointX":1157795117,"diPointY":357056021,"di_tag":"房地产 住宅区 小区",'
     '"dis":-1,"dist2route":0,"dist2start":0,'
     '"ext":{"detail_info":{"aoi":"内金沙","apartment_layout_introduction":"",'
     '"areaid":"631","building_time":"2006","business_scope":[{"name":"fangchan"}],'
     '"business_scope_type":"property","business_state":"","cn_state":"","developers":"雄宇实业",'
     '"display_info_comment_label":{"hotel":"","life":""},"display_info_redu":"4521","from_pds":"1",'
     '"guoke_geo":{"geo":""},"house_type":"板楼","image":'
     '"http:\/\/hiphotos.baidu.com\/map\/pic\/item\/dcc451da81cb39db132f7823db160924aa1830d3.jpg",'
     '"link":[],"mbc":{"markv":1,"shhouse":{"android":"9.1.0","ios":"9.1.0","loc":"2|15","params":"'
     '{"status":"1"}","reder_mode":"0","replace_id":"",'
     '"url":"http:\/\/mbcapi.baidu.com\/mbc\/plugin\/SecHandHouseView\/SecHandHouseView"}},'
     '"name":"印象金沙","new_tag":"","onrent_num":"","onsale_num":"","overall_rating":"3",'
     '"phone":"","poi_address":"青羊金阳路390号","point":{"x":11577951.17,"y":3570560.21},'
     '"price":"13874.0","price_change_rate":"0.0000","property_company":"","property_management_fee":"1.2",'
     '"property_right":"","rent_price":"2175","sales_info":[{"cn_name":"新浪二手房","onrent_num":"0",'
     '"onrent_url_PC":"http:\/\/cd.zufang.sina.com.cn\/info\/5218-4","onrent_url_mobile":"",'
     '"onsale_num":"0","onsale_url_PC":"http:\/\/cd.esf.sina.com.cn\/info\/5218-3",'
     '"onsale_url_mobile":"","selling_price":"6900",'
     '"url":"http:\/\/cd.esf.sina.com.cn\/info\/5218\/?pi=sina-place-esf&city=cd&key=5218&type=title",'
     '"url_mobilephone":"http:\/\/m.leju.com"},{"cn_name":null,"onrent_num":null,'
     '"onrent_url_PC":null,"onrent_url_mobile":null,"onsale_num":null,"onsale_url_PC":null,"onsale_url_mobile":null,'
     '"selling_price":null,'
     '"url":"http:\/\/cd.esf.sina.com.cn\/info\/5218\/?pi=sina-place-esf&city=cd&key=5218&type=title",'
     '"url_mobilephone":"http:\/\/m.leju.com"},{"cn_name":"新浪二手房","onrent_num":"0",'
     '"onrent_url_PC":"http:\/\/cd.zufang.sina.com.cn\/info\/6162-4","onrent_url_mobile":"","onsale_num":"0",'
     '"onsale_url_PC":"http:\/\/cd.esf.sina.com.cn\/info\/6162-3","onsale_url_mobile":"","selling_price":"7620",'
     '"url":"http:\/\/cd.esf.sina.com.cn\/info\/6162\/?pi=sina-place-esf&city=cd&key=6162&type=title",'
     '"url_mobilephone":"http:\/\/m.leju.com"},{"cn_name":"搜房网","onrent_num":"19","onrent_url_PC":"",'
     '"onrent_url_mobile":"","onsale_num":"19","onsale_url_PC":"","onsale_url_mobile":"","selling_price":"13874",'
     '"url":"http:\/\/yinxiangjinsha.fang.com\/?s=BaiDuSiteMapTest",'
     '"url_mobilephone":"http:\/\/m.fang.com\/xiaoqu\/cd\/3210403224.html?s=BaiDuSiteMapTest"},'
     '{"cn_name":null,"onrent_num":null,"onrent_url_PC":null,"onrent_url_mobile":null,"onsale_num":null,'
     '"onsale_url_PC":null,"onsale_url_mobile":null,"selling_price":null,'
     '"url":"http:\/\/cd.esf.sina.com.cn\/info\/6162\/?pi=sina-place-esf&city=cd&key=6162&type=title",'
     '"url_mobilephone":"http:\/\/m.leju.com"},{"cn_name":null,"onrent_num":null,"onrent_url_PC":null,'
     '"onrent_url_mobile":null,"onsale_num":null,"onsale_url_PC":null,"onsale_url_mobile":null,"selling_price":null,'
     '"url":null,"url_mobilephone":null},{"cn_name":"安居客","onrent_num":"0",'
     '"onrent_url_PC":"http:\/\/cd.zu.anjuke.com\/xiaoqu\/jingjiren\/142310","onrent_url_mobile":"",'
     '"onsale_num":"0","onsale_url_PC":"http:\/\/chengdu.anjuke.com\/community\/props\/sale\/142310",'
     '"onsale_url_mobile":"http:\/\/m.anjuke.com\/cd\/sale\/?comm_id=142310","selling_price":"7956",'
     '"url":"http:\/\/chengdu.anjuke.com\/community\/view\/142310","url_mobilephone":""},{"cn_name":'
     'null,"onrent_num":"8","onrent_url_PC":"http:\/\/chengdu.homelink.com.cn\/xiaoqu\/6603\/zf\/",'
     '"onrent_url_mobile":null,"onsale_num":"8",'
     '"onsale_url_PC":"http:\/\/chengdu.homelink.com.cn\/xiaoqu\/6603\/esf\/",'
     '"onsale_url_mobile":null,"selling_price":"7619","url":"http:\/\/chengdu.homelink.com.cn\/xiaoqu\/6603\/",'
     '"url_mobilephone":null},{"cn_name":null,"onrent_num":"0","onrent_url_PC":"","onrent_url_mobile":null,'
     '"onsale_num":"0","onsale_url_PC":"","onsale_url_mobile":null,"selling_price":"",'
     '"url":"http:\/\/data.house.sina.com.cn\/sc5663\/","url_mobilephone":null},{"cn_name":null,"onrent_num":null,'
     '"onrent_url_PC":null,"onrent_url_mobile":null,"onsale_num":null,"onsale_url_PC":null,'
     '"onsale_url_mobile":null,"selling_price":null,"url":null,"url_mobilephone":null},'
     '{"cn_name":null,"onrent_num":null,"onrent_url_PC":null,"onrent_url_mobile":null,"onsale_num":null,'
     '"onsale_url_PC":null,"onsale_url_mobile":null,"selling_price":null,"url":null,"url_mobilephone":null},'
     '{"cn_name":null,"onrent_num":null,"onrent_url_PC":null,"onrent_url_mobile":null,"onsale_num":null,'
     '"onsale_url_PC":null,"onsale_url_mobile":null,"selling_price":null,"url":null,"url_mobilephone":null}],'
     '"shop_hours_flag":"","tag":"内金沙","tag_info":'
     '"{"index_tag":"\u623f\u5730\u4ea7:10 \u4f4f\u5b85\u533a:10 \u5c0f\u533a:10",'
     '"show_tag":"\u4f4f\u5b85\u533a"}","volume_rate":"2.80"},"src_name":"house"},'
     '"ext_display":{"display_info":{"catalog_fields":[],"impression_tag":{"hotel":"","life":""},'
     '"redu":"4521","source_map":{"catalog":{"field_name":"poi_bank","priority":"0",'
     '"uid":"8674884642706708820","update_time":"1516264705.8391"}},"src_name":"display_info",'
     '"uids":["8674884642706708820:redu","8674884642706708820","6184753473620203062"]}},'
     '"ext_type":4,"f_flag":24,"father_son":0,"flag_type":"128",'
     '"geo":"1|11577951.17,3570560.21;11577951.17,3570560.21|11577951.17,3570560.21;",'
     '"geo_type":2,"indoor_pano":"","ismodified":0,"name":"印象金沙小区","navi_update_time":1519373652,'
     '"navi_x":"11577800.76","navi_y":"3570423.25","new_catalog_id":"100101","pano":1,"poiType":0,'
     '"poi_click_num":0,"poi_profile":1,"primary_uid":"8674884642706708820","prio_flag":32,"route_flag":0,'
     '"show_tag":[],"status":1,"std_tag":"房地产;住宅区","std_tag_id":"2403","storage_src":"api",'
     '"street_id":"3d108ba9878517f7ce04ef22","tag":"房地产 住宅区 <font color="#c60a00">小区<\/font>",']

"""
pattern = r'.+?(?=")'
adr = re.findall(pattern, r[0])
print('adr: %s \n' % adr)
pattern = r'\(.+?\['
add1 = re.sub(pattern, ' ', adr[0])
print("add1: %s \n" % add1)
pattern = r'\(.+?\]'
add2 = re.sub(pattern, ' ', add1)
print("add2: %s \n" % add2)  # 地址
# pattern = r'alias.*?]'
pattern = r'(?<=aoi.:.).+?(?=")'
alias = re.findall(pattern, r[0])
print('alias: %s \n' % alias)
"""

adr = "[四川省(32)|PROV|0|NONE][成都市(75)|CITY|0|NONE][青羊区(631)|AREA|1|NONE][西马棚街()|ROAD|1|NONE]30号"
_pattern = r'\(.+?\['
_address = re.sub(_pattern, '', adr)
print("address: %s" % _address)
_pattern = r'\(.+?\]'
_add2 = re.sub(_pattern, '', _address)
print("add2: %s" % _add2)


'''
r'(?<="phone":").+?(?=")'
(?<=@@！).*(?=@@~) 
"alias":["成都印象金沙","印象金沙小区"],
"name":"印象金沙小区",
'''

str1 = re.sub(':', '', str(datetime.now()))
print("1 %s" % str1)
str1 = re.sub('-', '', str1)
print("2 %s" % str1)
str1 = re.split('\.', str1)
print("3 %s" % str1[0])
str1 = re.sub(' ', '_', str1[0])
print("4 %s" % str1)
file_name = 'test_%s.xls' % str1
print("\n file_name: %s" % file_name)
# file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dic', file_name)
# print("\n file_dir: %s" % file_dir)
# xls_file = xlwt.open_workbook(file_dir)

_str = os.path.join(os.getcwd(), "dic", "baidu_result")
print("_con:", _str)


r1 = '0,"addr":"蜀鑫路8号海亮樾金沙5号楼","area":631,"area_name":"成都市青羊区","biz_type":0,"brand_id":null,' \
     '"catalogID":0,"cla":[],"click_flag":0,"detail":0,"diPointX":1157728399,"diPointY":357120427,' \
     '"di_tag":"幼儿园 学校 教育","dis":-1,"dist2route":0,"dist2start":0,"ext":"",' \
     '"ext_display":{"display_info":{"catalog_fields":[],"impression_tag":{"hotel":"","life":""},' \
     '"redu":"494","source_map":{"catalog":{"field_name":"poi_bank","priority":"0",' \
     '"uid":"7163384712694397029","update_time":"1506001629.7351"}},"src_name":' \
     '"display_info","uids":["7163384712694397029:redu","7163384712694397029"]}},' \
     '"ext_type":0,"f_flag":9,"father_son":0,"flag_type":"256",' \
     '"geo":"1|11577283.99,3571204.27;11577283.99,3571204.27|11577283.99,3571204.27;",' \
     '"geo_type":2,"name":"金沙蒙特梭利幼儿园","navi_update_time":1517790944,"navi_x":"0","navi_y":"0",' \
     '"new_catalog_id":"0d0101","poiType":0,"poi_click_num":0,"poi_profile":0,' \
     '"primary_uid":"7163384712694397029","prio_flag":32,"route_flag":0,"show_tag":[],' \
     '"status":1,"std_tag":"教育培训;幼儿园","std_tag_id":"1805","storage_src":"api","tag":' \
     '"<font color="#c60a00">幼儿园<\/font> 学校 教育","floor":"[["B3|B2|B1|F1|F2|F3"], ["23"], "", 0, ""]",' \
     ''


def _get_navi_x(r_split):
    """
    it's used for find the object's pix coordinate, it's means the x site of point on the map
    :param r_split: the input is a list
    :return: Name, the object's pix_x in the spider results
    """
    _r = r_split
    _p1 = r'(?<=navi_y.:.).+?(?=")'
    _x1 = re.findall(_p1, _r)
    print("x1:", _x1)
    _p2 = r'(?<="y":).+?(?=})'
    _x2 = re.findall(_p2, _r)
    _x2 = ['0' if _x == '"0"' else _x for _x in _x2]
    if len(_x2) == 0:
        _x2 = ['0']
    print("x2:", _x2)
    _p3 = r'(?<="geo":"1\|).+?(?=;)'
    _x3 = re.findall(_p3, _r)
    _x3 = re.split(r',', _x3[0])
    print("x3:", _x3)

    if _x1[0] and float(_x1[0]) > 0:
        _r_x = _x1[0]
    elif _x2[0] and float(_x2[0]) > 0:
        # _x2 = _x2[0].replace('\"', '')
        _r_x = _x2[0]
    elif _x3[1] and float(_x3[1]) > 0:
        _r_x = _x3[1]
    else:
        _r_x = 0.0
    return _r_x


_re = _get_navi_x(r1)
print("re: %s" % _re)

_r = '"area":631,"area_name":"成都市青羊区"'
_p1 = r'(?<=area_name.:.).+?(?=")'
_x1 = re.findall(_p1, _r)
print("x1: %s" % _x1)

local_url = os.path.join(os.path.abspath('..'), "dic", "mct2bd09.html")
print("local_url: %s" % local_url)

__t_name = 'School_info'
__sql = ('select Id, Pix_X, Pix_Y FROM %s WHERE BD_lat IS NULL OR BD_lng IS NULL' % __t_name)
print("__sql: %s" % __sql)

lat = '经度lat:30.670394;'
lat = re.findall(r'(?<=:).+?(?=;)', lat)
print("lat: %s" % lat)

__r = '"cla":[[17,"旅游景点"],[158,"<font color="#c60a00">公园<\/font>"]],"click_flag"'
__p = r'(?<="cla":.).+?(?=\],"click_flag")'
__cla = re.findall(__p, __r)
print("cla is %s" % __cla[0])
