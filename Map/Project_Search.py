# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.24
Description:
- this procedure is helping find the project in the city by the key word.
- input : region_code in the BaiDu Map (any level, just like city, village and so on );
- input : key word (just like project, store), if you want find some other type , may be you need change the
          function - _get_project_list()
- input: pn, means page number, it control the number in the results
- step: 1st, __get_proj_list to get the list of project which isn't include the area coordinate; 2nd, insert the record
        into db; 3rd, translate the project's point coordinate from mct to bd09; 4th, __get_proj_shape to get the
        project's area coordinate , then translate the coordinate list from mct to bd09 and insert into db.
"""


import requests, re, time, os
from Map.Public import proj_info, parameter_search, bd09_coordinate_object
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# define function that to get the list of the project
def __get_proj_list(region, kw, pn=10):
    """

    :param region: the city code where the objects inside, you can input code or name
    :param kw: the objects which you want to search
    :param pn: the page No.
    :return: the projects' attribute in the list
    """
    # define parameter
    __parameter = parameter_search()

    # define then csv file
    '''
    _csvFile = open(r'/Users/liaoying/Desktop/Python Project/Baidu/dic/%s.csv' % 'CityData', 'a+',
                    newline='', encoding='utf-8')
    _writer = csv.writer(_csvFile)
    _writer.writerow(('ID', 'project_name', 'alias', 'plate', 'p_x', 'p_y', 'add1', 'add2', 'developer', 'type',
                      'property', 'fee', 'phone'))
    '''

    # define the url and others
    __url = 'http://map.baidu.com/'
    __parameter["c"] = region
    __parameter["wd"] = kw
    __parameter["pn"] = pn
    __parameter["nn"] = __parameter["pn"] * 10
    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # translate code
        __pattern = r'(?<={"acc_flag.:).+?(?="ty":)'
        __r_list = re.findall(__pattern, __htm_code)
        __n = 0

        '''
        # write the record into file to find the attribute of projects
        f = open('/Users/liaoying/Desktop/PythonProject/Baidu/dic/community', 'w')
        f.write(_r_list[2])
        f.close()
        '''

        for __r in __r_list:
            __project = proj_info(__r)
            __n += 1
            print("\nproj_id: %s" % __project.id)
            print("proj_name: %s" % __project.name)
            print("proj_alias: %s" % __project.alias)
            print("proj_plate: %s" % __project.plate)
            print("proj_mctX: %s" % __project.mct_x)
            print("proj_mctY: %s" % __project.mct_y)
            print("proj_add1: %s" % __project.add1)
            print("proj_add2: %s" % __project.add2)
            print("proj_dev: %s" % __project.developer)
            print("proj_type: %s" % __project.type)
            print("proj_prop_com: %s" % __project.prop_company)
            print("proj_fee: %s" % __project.prop_fee)
            print("proj_area_x: %s" % __project.pix_area_x)
            print("proj_area_y: %s" % __project.pix_area_y)
            print("proj_area_code: %s" % __project.area_code)
            print("proj_area_name: %s" % __project.area_name)
            print("base_time: %s" % __project.base_update_time)
            print("navi_time: %s" % __project.point_update_time)
            print("street_id: %s" % __project.street_id)

        __m = __n
        return __m

    except ValueError as e:
        raise e
    finally:
        pass


def __get_proj_shape(street_id):
    """
    this is a function get the shape of project from web
    :param street_id: the street_id is the profile_id of project from the result of function which
           named _get_project_list(), it's a attribute of class (proj_info)
    :return: have two type. one is true, that means the return from requests is not empty, the value is a coordinate
             list which must translate from mct to bd09; one is false, that means no return from requests,
             the value is None .
    """
    __p_id = street_id
    __url = "http://map.baidu.com/"
    __parameter = {
        "b": "",
        "biz": "1",
        "c": "75",
        "da_par": "direct",
        "ext_ver": "new",
        "from": "webmap",
        "ie": "utf-8",
        "l": "12",
        "newmap": "1",
        "nn": "0",
        "pcevaname": "pc4.1",
        "qt": "ext",
        "reqflag": "pcmap",
        # "t":"",
        "tn": "B_NORMAL_MAP",
        # "u_loc":"11585297, 3568091"
        "uid": __p_id,
    }
    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }
    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')
        __pattern = r'(?<="content":.).+?(?=.},"current_city")'
        __r_list = re.findall(__pattern, __htm_code)

        if __r_list:
            __p1 = r'(?<=\|1-).+?(?=.","uid")'
            __r = re.findall(__p1, __r_list[0])
            __coor_str = __r[0]
            __coor_list = __coor_str.split(",")
            __m = 0
            __n = 1
            __proj_geo = []
            while __n <= len(__coor_list):
                __coor = [__coor_list[__m], __coor_list[__n]]
                __proj_geo.append(__coor)
                __m = __m + 2
                __n = __n + 2
        else:
            __proj_geo = None

        print(__proj_geo)
        return __proj_geo
    except ValueError as e:
        raise e
    finally:
        pass


def __proj_search(region, kw, n):
    """

    :param region: the city code where the objects inside, you can input code or name
    :param kw: he objects which you want to search
    :param n: the page No.
    :return: no return
    """
    __region = region
    __kw = kw
    __n = int(n)
    __start = time.time()
    __num = 1
    __s = 0

    for __page in range(__n):
        __m = __get_proj_list(__region, __kw, __page)  # 防止访问频率太高，避免被百度公司封
        time.sleep(2)
        if __num % 20 == 0:
            time.sleep(4)
        if __num % 100 == 0:
            time.sleep(6)
        if __num % 200 == 0:
            time.sleep(8)
        __num = __num + 1
        __s = __s + __m

    __end = time.time()
    __last_time = int((__end-__start))
    print('\n 共耗时 %s s, 获取 %s 页，%s 条数据！' % (str(__last_time), __num-1, __s))


def __proj_mct_2_bd09(proj_geo: list):
    """
    This function is used for translate project's area coordinate from mct to bd09
    :param proj_geo: the list of project's area coordinate
    :return: None
    """
    __proj_shape_mct = proj_geo
    __proj_shape_bd09 = []
    __firefox_options = Options()
    __firefox_options.add_argument('-headless')  # use the headless model(not GUI)
    __driver = Firefox(executable_path='geckodriver', firefox_options=__firefox_options)
    # if open local html file in the browser, must add the header - "file://",
    # you'll get the malformed url wrong
    __local_url = "file://" + os.path.join(os.path.abspath('..'), "dic", "mct2bd09.html")
    __driver.get(__local_url)
    print("the initialize page title is:  ", __driver.title)

    for __geo_m in __proj_shape_mct:
        __pix_x = __geo_m[0]
        __pix_y = __geo_m[1]
        time.sleep(3)
        __driver.find_element_by_id('mctX').clear()
        __driver.find_element_by_id('mctY').clear()
        __driver.find_element_by_id('mctX').send_keys(__pix_x)
        __driver.find_element_by_id('mctY').send_keys(__pix_y)
        __driver.find_element_by_xpath("//div[2]/p[6]/input[1]").click()
        time.sleep(3)
        __db09_lat = __driver.find_element_by_xpath("//p[@id=\"pointX\"]").text
        __db09_lat = re.findall(r'(?<=:).+?(?=;)', __db09_lat)[0]
        __db09_lng = __driver.find_element_by_xpath("//p[@id=\"pointY\"]").text
        __db09_lng = re.findall(r'(?<=:).+?(?=;)', __db09_lng)[0]
        __address = __driver.find_element_by_xpath("//p[@id=\"entertaiment\"]").text
        __address = re.sub(r', ', '', __address)
        __bd_coor = bd09_coordinate_object(None, __db09_lat, __db09_lng, __address)
        __shape_bd09 = [__bd_coor.lng, __bd_coor.lat]
        __proj_shape_bd09.append(__shape_bd09)

        print("\n")
        print("纬度Lat: %s" % __bd_coor.lat)
        print("经度Lng: %s" % __bd_coor.lng)
        print("address: %s" % __bd_coor.address)

    print("\n bd09: %s" % __proj_shape_bd09)
    __driver.quit()


'''

# test code
_get_project_list("631", "小区", 2)


# __proj_search("631", "小区", 2)
# __get_proj_shape("82061b7f137f08c2ed74f823")

__proj_shape = [['11573980.55', '3568447.03'], ['11574101.0', '3568446.52'], ['11574118.48', '3568538.47'],
                ['11574185.05', '3568541.04'], ['11574192.12', '3568384.89'], ['11574194.82', '3568359.98'],
                ['11574197.21', '3568339.04'], ['11574197.49', '3568319.26'], ['11574198.19', '3568285.16'],
                ['11574198.71', '3568247.51'], ['11574199.51', '3568195.02'], ['11574198.07', '3568182.52'],
                ['11574135.51', '3568184.06'], ['11574031.09', '3568182.52'], ['11573976.1', '3568183.03'],
                ['11573976.35', '3568251.22'], ['11573974.85', '3568337.76'], ['11573975.15', '3568408.2'],
                ['11573980.55', '3568447.03']]
__proj_mct_2_bd09(__proj_shape)


'''