# -*- coding: utf-8 -*-
"""

Author: Wayne
Ver: v0.1
Date: 2018.02.25
Description:
- this procedure is helping translate the mercator to the wgs84.
- https://www.cnblogs.com/reboot777/p/7124010.html

"""

import math


def mercator2wgs84(mercator):
    # key1=mercator.keys()[0]
    # key2=mercator.keys()[1]
    point_x = mercator[0]
    point_y = mercator[1]
    x = point_x / 20037508.3427892 * 180
    y = point_y / 20037508.3427892 * 180
    y = 180 / math.pi * (2 * math.atan(math.exp(y * math.pi / 180)) - math.pi / 2)
    return x, y


# test code: 成都市鼓楼小学
mercator = (11586260.2779, 3568139.31197)
p_x, p_y = mercator2wgs84(mercator)
print(p_x, ',', p_y)