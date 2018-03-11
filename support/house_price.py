# -*- coding: utf-8 -*-

import math, random
from random import Random

''' =======define the procedure of price translate to the string========= '''


def _price_math(price):
    """

    :param price: the input of price
    :return: _n, _price
    """
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


def _price_encrypt(len_p, val_p):
    """

    :param len_p: the length of price
    :param val_p: the value of price
    :return:
    """
    _len_price = len_p
    _price = list(val_p)
    _n_count = 1
    __order_random = []
    _i_len = 30 - _len_price

    # get the order number of price member in the string
    while _n_count <= _len_price:
        _r = random.randint(1, 23)  # 9 instead of _i_len
        if _r not in __order_random:
            __order_random.append(_r)
            _n_count += 1

    # get the random string which is mixed of num and char
    _id = ''
    _chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    _length = len(_chars) - 1
    _str_random = Random()

    for _i in range(_i_len - 1):
        _id += _chars[_str_random.randint(0, _length)]

    for _num in __order_random:
        _num = _num + 64
        _c_order = chr(_num)
        _id = _id + _c_order

    # join the order and string
    _id = list(_id)
    _s = 0
    for _i in __order_random:
        _id[_i] = _price[_s]
        _s = _s + 1
    _id = ''.join(_id) + chr(_len_price + 64)

    # print("_id: %s" % _id)
    return _id


def price_encr(price):
    __price = price
    __n, __price = _price_math(__price)
    _id = _price_encrypt(__n, __price)
    return _id, __price


''' ======define the procedure of string translate to price ==============='''


# b64PAMTI1qENJHENt3qUjly8EAHWBD
def price_decrypt(str_price):
    """

    :param str_price:
    :return:
    """
    _str_price = list(str_price)
    _end_str = _str_price[-1]
    _len_price = ord(_end_str) - 64  # get the length of price

    # get the order of price
    _list_price = _str_price[-(_len_price+1):-1]
    _price = []
    for _list in _list_price:
        _num = ord(_list) - 64
        _price.append(_str_price[_num])
    _price = ''.join(_price)

    # return the value of price
    _price = int(_price)
    _price1 = round(math.e ** (pow(_price, 1/4)))
    return _price1


fid, price1 = price_encr(18100)
print('fid: %s' % fid)
print('the adjust price is %s' % price1)
price2 = price_decrypt(fid)
print('the value of price is %s' % price2)

