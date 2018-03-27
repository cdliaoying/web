# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.15
Description:
- this file develop some functions to simulate one js page which can translate Baidu's pix coordinate
  to the BD09's coordinate by the Baidu's API
"""
import os, time, re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from Map.Public import _get_objects_id, bd09_coordinate_object, _write_bd09_sql


''' ======= use phantomjs to open local page ============ '''

'''
driver = webdriver.PhantomJS()
driver.get("/Users/liaoying/Desktop/PythonProject/Baidu/dic/mct2bd09.html")
print(driver.title)
print(driver.current_url)
print(driver.name)
'''

''' ======= use headless type open the website   ============'''


def __pix_2_bd09(object_name: str, pix_coord: list):
    """

    :param object_name: the table's name in the database
    :param pix_coord: the record list in the table
    :return: the number of updated record
    """

    # initialize the firefox page in headless model
    __object_name = object_name
    __pix_coor = pix_coord
    __firefox_options = Options()
    __firefox_options.add_argument('-headless')  # use the headless model(not GUI)
    __driver = Firefox(executable_path='geckodriver', firefox_options=__firefox_options)
    # if open local html file in the browser, must add the header - "file://",
    # you'll get the malformed url wrong
    __local_url = "file://" + os.path.join(os.path.abspath('..'), "dic", "mct2bd09.html")
    __driver.get(__local_url)
    __i = 0
    print("the initialize page title is:  ",__driver.title)

    # translate the object of pix coordinate in the list to the Bd09 coordinate
    for __c in __pix_coor:
        __id = __c.id
        __pix_x = __c.pix_x
        __pix_y = __c.pix_y
        time.sleep(5)
        __driver.find_element_by_id('mctX').clear()
        __driver.find_element_by_id('mctY').clear()
        __driver.find_element_by_id('mctX').send_keys(__pix_x)
        __driver.find_element_by_id('mctY').send_keys(__pix_y)
        __driver.find_element_by_xpath("//div[2]/p[6]/input[1]").click()
        time.sleep(5)
        __db09_lat = __driver.find_element_by_xpath("//p[@id=\"pointX\"]").text
        __db09_lat = re.findall(r'(?<=:).+?(?=;)', __db09_lat)[0]
        __db09_lng = __driver.find_element_by_xpath("//p[@id=\"pointY\"]").text
        __db09_lng = re.findall(r'(?<=:).+?(?=;)', __db09_lng)[0]
        __address = __driver.find_element_by_xpath("//p[@id=\"entertaiment\"]").text
        __address = re.sub(r', ', '', __address)

        __bd_coor = bd09_coordinate_object(__id, __db09_lat, __db09_lng, __address)

        __i = __i + 1
        print("\n")
        print("纬度Lat: %s" % __bd_coor.lat)
        print("经度Lng: %s" % __bd_coor.lng)
        print("address: %s" % __bd_coor.address)
        #  __driver.close()

        _write_bd09_sql(__object_name, __bd_coor)

    __driver.quit()
    return __i


def get_object_bd09():
    """

    :return:
    """
    __object_name = 'school_info' # object_name is the talbe name in the sqlite
    __pix_c = _get_objects_id(__object_name)
    print("共有 %s 条数据需要转换BD09坐标" % len(__pix_c))
    if __pix_c:
        __i = __pix_2_bd09(__object_name, __pix_c[0:11])
        print("\n共转换 %s 条数据" % __i)
    pass


#  test code
get_object_bd09()
