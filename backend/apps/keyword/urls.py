#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/18 16:13
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from apps.keyword.handler import GetKeywordHandler, GetKeywordListByAdgroupHandle
from tornado.web import url

urlpatten = [
    # 根据 推广单元id 获取其对应100条关键词
    # url('/get/keyword/(\d+)/', GetKeywordHandler),
    # 添加关键词
    # url('/post/keyword/', GetKeywordHandler),
    # 根据 推广单元id 获取关键词列表
    # url('/get/keywordlist/(\d+)/', GetKeywordListByAdgroupHandle)
]
