#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/16 23:40
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.adgroup.handler import CreateAdgroupHandler, UpdateAdgroupStatusHandler, DeleteAdgroupHandler

urlpatten = [
    # 创建推广单元
    # url('/post/adgroup/', CreateAdgroupHandler),
    # 根据推广计划id获得其所有推广单元
    # url('/get/adgroup/(\d+)/(\d+)/', CreateAdgroupHandler),
    # 更新推广单元状态
    # url('/update/adgroup/status/', UpdateAdgroupStatusHandler),
    # 删除推广单元
    # url('/delete/adgroup/', DeleteAdgroupHandler)
]
