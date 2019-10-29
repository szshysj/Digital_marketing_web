#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/29 11:03
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.test_api.handler import TestHandler, Test1Handler

urlpatten = [
    url('/test/', TestHandler),
    url('/test1/', Test1Handler)
]
