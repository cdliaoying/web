# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.28
Description:
- this procedure is helping find the metro station in the city by the key word.
- input : line_id, this is the record's id from baidu js' content;

"""

import requests, re, os, sqlite3
from Map.Public import matro_line_info, station_info, _dict_factory
from Map.webkit import get_object_bd09


def __get_line_info(line_id):
    """

    :return _m:
    """
    # define parameter
    __parameter = {
        "c": "75",
        "newmap": "1",
        "qt": "bsl",
        "tps": "",
        "uid": "",  # line_id
    }

    # define the url and others
    __url = 'http://map.baidu.com/'
    __parameter["uid"] = line_id

    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')  # 转码
        __pattern = r'(?<="kindtype":).+?(?="current_city":)'
        __r_line = re.findall(__pattern, __htm_code)  # 按段落匹配

        if __r_line:
            __line_info = matro_line_info(__r_line[0])
            # add sql for insert database
            # school_write_sql(_school)
            print("\n")
            print("line_id: %s" % __line_info.line_id)
            print("line_name: %s" % __line_info.line_name)
            print("max_price: %s" % __line_info.max_price)
            print("line_tiem: %s" % __line_info.line_time)
            print("line_color: %s" % __line_info.line_color)
            print("creat_time: %s" % __line_info.creat_date)
        else:
            print("It's not get line info!")

        if __r_line:
            __dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
            __con = sqlite3.connect(__dir)
            __con.row_factory = _dict_factory
            __cur = __con.cursor()
            __cur.execute("SELECT count(line_id) AS num FROM metro_line_info "
                          "WHERE line_id = ?", (__line_info.line_id,))
            __r = __cur.fetchall()
            if __r[0]["num"] == 0:
                __cur.execute("INSERT INTO metro_line_info "
                              "VALUES(?, ? , ?, ?, ?, ?) ",
                              (__line_info.line_id, __line_info.line_name,
                               __line_info.max_price, __line_info.line_time,
                               __line_info.line_color, __line_info.creat_date))
                __con.commit()
                print("写入成功！")
            else:
                print("\n%s, %s 已存在!" % (__line_info.line_id, __line_info.line_name))
            __con.close()

    except ValueError as e:
        raise e
    finally:
        pass


# test code
# __get_line_info("80daf0912b34edb2441a3221")


def __get_station_info(line_id):
    """

    :param line_id: the id of metro lines' record
    :return:
    """
    # define parameter
    __parameter = {
        "c": "75",
        "newmap": "1",
        "qt": "bsl",
        "tps": "",
        "uid": "",  # 1号线id
    }

    # define the url and others
    __url = 'http://map.baidu.com/'
    __parameter["uid"] = line_id
    __headers = {
        "Host": "map.baidu.com",
        "Referer": "https://map.baidu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0",
    }

    try:
        __htm_get = requests.get(__url, params=__parameter, headers=__headers, timeout=6)
        print("\n the requests' status is %s \n" % __htm_get.raise_for_status())
        __htm_code = __htm_get.text.encode('latin-1').decode('unicode_escape')
        __pattern = r'(?<="stations":).+?(?=,"ticketPrice":)'
        __r_st = re.findall(__pattern, __htm_code)
        __pattern = r'(?<="geo":).+?(?=},{"geo":)'
        __r_station = re.findall(__pattern, __r_st[0])

        if __r_station:
            __dir = os.path.join(os.path.abspath('..'), "dic", "baidu_result")
            __con = sqlite3.connect(__dir)
            __con.row_factory = _dict_factory
            __cur = __con.cursor()
            __c = 0

            for __r in __r_station:
                __station_info = station_info(__r, __parameter["uid"])
                print("\n")
                print("line_id: %s" % __station_info.line_id)
                print("station_id: %s" % __station_info.st_id)
                print("station_name: %s" % __station_info.st_name)
                print("station_start_time: %s" % __station_info.st_start_time)
                print("station_end_time: %s" % __station_info.st_end_time)
                print("station_subway: %s" % __station_info.st_subway)
                print("station_transfer: %s" % __station_info.st_transfer)
                print("station_pix_x: %s" % __station_info.st_pix_x)
                print("station_pix_y: %s" % __station_info.st_pix_y)
                print("creat_date: %s" % __station_info.creat_date)

                __cur.execute("SELECT count(Id) AS num FROM metro_station_info "
                              "WHERE Id = ?", (__station_info.st_id,))
                __r = __cur.fetchall()
                if __r[0]["num"] == 0:
                    __cur.execute("INSERT INTO metro_station_info "
                                  "(Id, line_id , st_name, start_time, end_time, subway, "
                                  "transfer, Pix_X , Pix_Y, creat_date) "
                                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                                  (__station_info.st_id, __station_info.line_id,
                                   __station_info.st_name, __station_info.st_start_time,
                                   __station_info.st_end_time, __station_info.st_subway,
                                   __station_info.st_transfer, __station_info.st_pix_x,
                                   __station_info.st_pix_y, __station_info.creat_date))
                    __con.commit()
                    print("写入成功！")
                    __c = __c + 1
                else:
                    print("\n%s, %s 已存在!" % (__station_info.st_id, __station_info.st_name))
            __con.close()
            print("\n 共写入 %s 条记录!" % __c)
        else:
            print("It's not get ths station info!")
    except ValueError as e:
        raise e
    finally:
        pass


# get station info
# __get_station_info("80daf0912b34edb2441a3221")
# translate mct to bd09
# get_object_bd09("metro_station_info")

