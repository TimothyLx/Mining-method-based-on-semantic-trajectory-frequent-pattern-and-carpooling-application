# -*- coding:utf-8 -*-
# @FileName:distance_calculate.py
# @Time    :2020/7/615:41
# @Author  :LX

from math import radians, cos, sin, asin, sqrt
def DIST(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000
