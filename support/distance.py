# -*- coding: UTF-8 -*-

"""

Author: Wayne
Ver: v0.0.1
Date: 2018.05.08
Description:
- this module is saving some public function

"""

from math import sin, asin, cos, radians, fabs, sqrt


def coor_dis(lng_name: str, lat_name: str, lng_addr: str, lat_addr: str):
    """ used for computing the distance of two points

    :param
        lng_name {str} - the lng of point A
        lat_name {str} - the lat of point A
        lng_addr {str} - the lng of point B
        lat_addr {str} - the lat of point B
    :return
        distance {float} - the distance of two points
    """
    __radius = 6371

    try:
        if lng_name is not None and lat_name is not None and lng_addr is not None \
                and lat_addr is not None:
            __lat0 = radians(float(lat_name))
            __lng0 = radians(float(lng_name))
            __lat1 = radians(float(lat_addr))
            __lng1 = radians(float(lng_addr))

            __dlng = fabs(__lng0 - __lng1)
            __dlat = fabs(__lat0 - __lat1)

            __h = sin(__dlat / 2) * sin(__dlat / 2) + cos(__lat0) * cos(__lat1)\
                  * sin(__dlng / 2) * sin(__dlng / 2)
            __dintance = 2 * __radius * asin(sqrt(__h))
            return round(__dintance, 10)
        else:
            return None
    except Exception as e:
        raise e
    finally:
        pass


if __name__ == "__main__":
    # 104.0895500000,30.5973960000;104.0894770000,30.5976530000
    # 0.0294189156
    distance = coor_dis('104.0895500000', '30.5973960000', '104.0894770000', '30.5976530000')
    print("distance is %s" % distance)
