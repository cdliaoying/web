# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.04.08
Description:
- this procedure is getting the school list from educational website.


"""

import requests, re, time, os, sqlite3, lxml
from bs4 import BeautifulSoup
from Map.Public import school_info, parameter_search, _dict_factory


def __get_education_list(page_no: int):
    __page_no = page_no
    __url = 'http://infomap.cdedu.gov.cn/Home/Index'
    __parameter = {
        "all": ""
    }
    __headers = {
        "Host": "infomap.cdedu.gov.cn",
        "Referer": "http://infomap.cdedu.gov.cn/Home/Index?all=1&pages=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }
    __parameter["all"] = __page_no

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text

        '''
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/gov/education', 'w')
        f.write(__htm_code)
        f.close()
        '''

        __htm_content = BeautifulSoup(__htm_code, "lxml")
        print(__htm_content)

    except ValueError as e:
        raise e
    finally:
        pass


__get_education_list(1)