#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/15 0:45
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from wtforms_tornado import Form
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, AnyOf


class AddCampaignForm(Form):
    campaign_name = StringField('推广计划名称', validators=[
        DataRequired(message='请输入推广计划名称'),
        Length(min=1, max=40, message='推广计划名称长度要求在1到40之间')
    ])

    budget = FloatField('计划预算', validators=[
        DataRequired(message='请输入计划预算'),
        NumberRange(min=60, max=999999, message='计划预算必须大于等于60元, 小于等于999999元')
    ])

    promoteArea = StringField('推广地域', validators=[DataRequired(message='请选择计划投放区域')])

    schedule = IntegerField('推广时段', validators=[
        DataRequired(message='请选择推广时段'),
        AnyOf(values=[1, 2, 3, 4, 5, 6, 7, 8, 9], message='请选择正确的推广时段类型')
    ])

    cositeFlag = StringField('站外推广', validators=[
        DataRequired(message='请输入站外推广'),
        AnyOf(values=['0', '1'], message='请选择正确的站外推广类型')
    ])


class UpdateCampaignStatusForm(Form):
    campaignId = IntegerField('推广计划id', validators=[
        DataRequired(message='请输入推广ID'),
        NumberRange(min=100000000, max=999999999, message='请输入正确的推广ID')
    ])
    status = StringField('推广计划状态', validators=[
        DataRequired(message='请输入状态信息'),
        AnyOf(values=['0', '1'], message='请输入正确的状态')
    ])


class UpdateCampaignForm(Form):
    campaignId = IntegerField('推广计划id', validators=[
        DataRequired(message='请输入推广ID'),
        NumberRange(min=100000000, max=999999999, message='请输入正确的推广ID')
    ])

    budget = FloatField('计划预算', validators=[
        DataRequired(message='请输入计划预算'),
        NumberRange(min=60, max=999999, message='计划预算必须大于60元, 小于999999元')
    ])

    promoteArea = StringField('计划投放区域', validators=[DataRequired(message='请选择计划投放区域')])

    schedule = IntegerField('计划投放时段', validators=[
        DataRequired(message='请选择计划投放时段'),
        AnyOf(values=[1, 2, 3, 4, 5, 6, 7, 8, 9], message='请选择正确的计划时段投放类型')
    ])

    cositeFlag = StringField('是否支持站外推广', validators=[
        DataRequired(message='请选择是否支持站外推广'),
        AnyOf(values=['0', '1'], message='请选择正确的站外推广类型')
    ])
