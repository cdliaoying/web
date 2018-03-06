# -*- coding: utf-8 -*-
import re, xlrd, xlwt, os
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