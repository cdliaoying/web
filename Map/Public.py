# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.02.26
Description:
- this file include some public function and class


"""


class mct_point():
    """
    -   usage: format mct_point
    -   attribute: mct_x(lon), mct_y(lat)
    """

    @property
    def mct_x(self):
        return self._mct_x

    @mct_x.setter
    def flag(self, v_mct_x):
        self._mct_x = v_mct_x

    @property
    def mct_y(self):
        return self._mct_y

    @mct_y.setter
    def flag(self, v_mct_y):
        self._mct_y = v_mct_y


class school():
    """
    -   usage: format school result
    -   attribute: ID, Name, Alias, Aoi, Mct_x, Mct_y, Add1, Add2, Type(Tag)
    """

    def __init__(self, ID, Name, Alias, Aoi, Mct_x, Mct_y, Add1, Add2, Type):
        self.ID = ID
        self.Name = Name
        self.Alias = Alias
        self.Aoi = Aoi
        self.Mct_x = Mct_x
        self.Mct_y = Mct_y
        self.Add1 = Add1
        self.Add2 = Add2
        self.Type = Type

    @property
    def pix_area_code(self):
        _area_code = dict(x=0, y=0, zoom=0)
        _area_code["x"] = int(self.Mct_x / 256)
        _area_code["y"] = int(self.Mct_y / 256)
        _area_code["zoom"] = 18
        return _area_code


_school = school
_school.Mct_x = 11586260.2779
_school.Mct_y = 3568139.31197
print(_school.pix_area_code)
