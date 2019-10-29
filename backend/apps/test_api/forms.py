#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/29 11:04
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from wtforms_tornado import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class Test1Form(Form):
    filed1 = StringField('测试字段1', validators=[
        DataRequired(message='请输入字符')
    ])

    filed2 = StringField('测试字段2', validators=[
        # DataRequired(message='请输入字符')
    ])
