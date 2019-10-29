#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/15 0:45
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from wtforms_tornado import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class GetOfferForm(Form):
    page_num = IntegerField('分页', validators=[
        DataRequired(message='请填写正确的分页'),
        NumberRange(min=1, max=4000, message='分页最小必须是1, 最大是4000')
    ])
