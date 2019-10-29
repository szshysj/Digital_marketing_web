#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 20:48
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from datetime import datetime
from Digital_marketing.settings import database

from peewee import Model, DateTimeField


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        database = database  # 与数据库做关联
