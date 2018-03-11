# -*- coding: utf-8 -*-

import math, random, re
from random import Random


def _price_format(price):
    _price = int(price)
    _price = int(math.log(_price) ** 4)
    _price = str(_price)
    _n = len(_price)
    return _n, _price

'''
# test code
n, price = _price_format(7000)
print("step 1：", n, ' ', price)
'''


def _price_rule(n, p):
    _n = n
    _price = list(p)
    _m = 1
    _random = []

    # get the order number of price member in the string
    while _m <= _n:
        _r = random.randint(1, 9)
        if _r not in _random:
            _random.append(_r)
            _m = _m + 1

    print("_random: %s" % _random)
    print("price %s" % _price)

    # get the string

    _id = ''
    _chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    _length = len(_chars) - 1
    _random1 = Random()
    for i in range(30):
        _id += _chars[_random1.randint(0, _length)]

    print("_id: %s" % _id)
    _id = list(_id)
    _s = 0
    for _i in _random:
        _id[_i] = _price[_s]
        _s = _s + 1
    _id = ''.join(_id) + ''.join(str(_n) for _n in _random)
    print("_id: %s" % _id)


n = 5
p = '16100'
_price_rule(n, p)
