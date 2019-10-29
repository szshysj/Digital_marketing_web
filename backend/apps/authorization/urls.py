#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 19:52
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.authorization.handler import GetCodeHandler

urlpatten = [
    # 获取code + 授权 + 保存用户信息入库
    url('/get/authorization/', GetCodeHandler)
]
