#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 23:28
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.area.handler import GetAreaHandler

urlpatten = [
    # 获取所有可投放地域列表
    url('/get/area/', GetAreaHandler)
]
