#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/18 15:38
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from wtforms_tornado import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class GetAdgroupKeywordHandler(Form):
    adGroupId = IntegerField('指定的推广单元ID', validators=[
        DataRequired(message='请输入指定的推广单元id'),
        NumberRange(min=1, message='请输入指定的推广单元ID')])
