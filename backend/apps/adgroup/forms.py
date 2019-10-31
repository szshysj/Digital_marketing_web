#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/17 10:18
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from wtforms_tornado import Form
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, AnyOf


class DeleteAdgroupHandlerForm(Form):
    adGroupId = IntegerField('推广计划id', validators=[
        DataRequired(message='请输入推广计划id'),
        NumberRange(min=100000000, max=999999999, message='请输入正确范围的推广计划id')
    ])


class UpdateAdgroupStatusForm(Form):
    campaignId = IntegerField('推广计划id', validators=[
        DataRequired(message='请填写推广计划id'),
        NumberRange(min=100000000, max=999999999, message='请填写正确的推广计划长度')
    ])
    adGroupId = IntegerField('推广单元id', validators=[
        DataRequired(message='请填写推广单元id'),
        NumberRange(min=100000000, max=999999999, message='请填写正确的推广单元长度')
    ])
    onlineState = StringField('推广单元状态', validators=[
        DataRequired(message='请填写推广单元状态'),
        AnyOf(values=['0', '1'], message='请填写正确的推广单元状态')
    ])


class CreateAdgroupForm(Form):
    campaignId = StringField('计划id', validators=[
        DataRequired(message='请输入计划id'),
        Length(min=6, max=10)])

    bidPrice = FloatField('推广单元默认出价', validators=[
        DataRequired(message='请输入推广单元默认出价'),
        NumberRange(min=0.3, message='推广单元默认出价不能低于0.3元')
    ])

    offerId = StringField('商品id', validators=[
        DataRequired(message='请输入商品id'),
        Length(min=8, max=14, message='请输入正确的商品id长度')])


class GetAdgroup(Form):
    campaignId = IntegerField('推广计划id', validators=[
        DataRequired(message='请输入推广计划id'),
        NumberRange(min=100000000, max=999999999, message='请输入正确的推广计划ID')
    ])

    pageNo = IntegerField('分页', validators=[
        DataRequired(message='请输入正确的页码'),
        NumberRange(min=1, message='页面至少从第一页开始')
    ])
