# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.04.08
Description:
- this procedure is getting the school list from educational website.


"""

import requests, re, time, os, sqlite3
from lxml import etree
from Map.Public import school_info, parameter_search, _dict_factory


def __get_education_list(tol_page: int):
    __i = 0
    __tol_page = tol_page + 1
    __url = 'http://infomap.cdedu.gov.cn/Home/Index'
    __parameter = {
        "all": ""
    }
    __headers = {
        "Host": "infomap.cdedu.gov.cn",
        "Referer": "http://infomap.cdedu.gov.cn/Home/Index?all=1&pages=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        for __cur_page in range(1, __tol_page):
            __parameter["all"] = __cur_page
            __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
            print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
            __htm_code = __htm_get.text

            '''
            f = open('/Users/liaoying/Desktop/PythonProject/Baidu/gov/education', 'w')
            f.write(__htm_code)
            f.close()
            '''

            ''' ---- tranlate jason str to html file ------'''
            __htm_content = etree.HTML(__htm_code)

            ''' ----- get the school info in the html -------'''
            __school_num = __htm_content.xpath("//ul[@class='index_ul01']")
            if __school_num:
                for __m in range(1, len(__school_num)+1):
                    for __n in range(1, 3):
                        __i += 1

                        # get school name
                        __url_name = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/a/h1" % (__m, __n)
                        __str_name = __htm_content.xpath(__url_name)
                        if __str_name:
                            __school_name = __str_name[0].text
                        else:
                            __school_name = None

                        # get school id
                        __url_id = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/a/@href" % (__m, __n)
                        __id_list = __htm_content.xpath(__url_id)
                        if __id_list:
                            __id_list[0] = __id_list[0] + ";"
                            __p_id = r'(?<=Id\=).+?(?=;)'
                            __id_list = re.findall(__p_id, __id_list[0])
                            __school_id = __id_list[0]
                        else:
                            __school_id = None

                        # get school level
                        __url_level = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[1]" % (__m, __n)
                        __level_list = __htm_content.xpath(__url_level)
                        if __level_list:
                            __school_level = __level_list[0].text
                            __p_level = r'【学段】'
                            __school_level = re.sub(__p_level, '', __school_level)
                        else:
                            __school_level = None

                        # get school area
                        __url_area = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[2]" % (__m, __n)
                        __area_list = __htm_content.xpath(__url_area)
                        if __area_list:
                            __school_area = __area_list[0].text
                            __p_area = r'【区域】'
                            __school_area = re.sub(__p_area, '', __school_area)
                        else:
                            __school_area = None

                        # get school type
                        __url_type = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[3]" % (__m, __n)
                        __type_list = __htm_content.xpath(__url_type)
                        if __type_list:
                            __school_type = __type_list[0].text
                            __p_type = r'【性质】'
                            __school_type = re.sub(__p_type, '', __school_type)
                        else:
                            __school_type = None

                        # get school phone
                        __url_phone = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[4]" % (__m, __n)
                        __phone_list = __htm_content.xpath(__url_phone)
                        if __phone_list:
                            __school_phone = __phone_list[0].text
                            __p_phone = r'【电话】'
                            __school_phone = re.sub(__p_phone, '', __school_phone)
                        else:
                            __school_phone = None

                        # get school addr
                        __url_addr = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[5]" % (__m, __n)
                        __addr_list = __htm_content.xpath(__url_addr)
                        if __addr_list:
                            __school_addr = __addr_list[0].text
                            __p_addr = r'【地址】'
                            __school_addr = re.sub(__p_addr, '', __school_addr)
                        else:
                            __school_phone = None

                        # get school website
                        __url_site = "//ul[@class='index_ul01']/../ul[%s]/li[%s]/div[2]/p[6]/a" % (__m, __n)
                        __site_list = __htm_content.xpath(__url_site)
                        if __site_list:
                            __school_site = __site_list[0].text
                        else:
                            __school_site = None


                        print("\n")
                        print("No: %s" % __i)
                        print("school_id: %s" % __school_id)
                        print(__school_name)
                        print(__school_level)
                        print(__school_area)
                        print(__school_type)
                        print(__school_phone)
                        print(__school_addr)
                        print(__school_site)





    except ValueError as e:
        raise e
    finally:
        pass


__get_education_list(1)
