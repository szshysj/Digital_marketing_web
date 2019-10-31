#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:37
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.offer.handler import GetOfferHandler

urlpatten = [
    # 获取用户商品列表
    url('/get/offer/(\\d{9})/(\\d+)/', GetOfferHandler)
]
