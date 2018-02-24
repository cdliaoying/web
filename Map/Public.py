# -*- coding: utf-8 -*-
import requests
import re

parameter = {
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
    "t": "1468896652886"
}


def _get_keyword(city, kw, pn=10):
    url = 'http://map.baidu.com/'
    parameter["c"] = city
    parameter["wd"] = kw
    parameter["pn"] = pn
    parameter["nn"] = parameter["pn"] * 10
    htm = requests.get(url, params=parameter)
    htm = htm.text.encode('latin-1').decode('unicode_escape')  # 转码
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    htm = re.findall(pattern, htm)  # 按段落匹配
    f = open('/Users/liaoying/Desktop/Python Project/Baidu/dic/community', 'w')
    f.write(htm[2])
    f.close()
    for r in htm:
        pattern = r'(?<=\b"\},"name":").+?(?=")'
        name = re.findall(pattern, r)
        if not name:
            pattern = r'(?<=\b,"name":").+?(?=")'
            name = re.findall(pattern, r)
        print(name[0])  # 名称

        pattern = r'.+?(?=")'
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)
        print(address)  # 地址

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        print(phone[0])  # 电话


_get_keyword("青羊区", "小区", 2)