#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/12 23:47
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.models import BaseModel
from datetime import datetime

from peewee import IntegerField, FixedCharField, SmallIntegerField, DateTimeField


class User(BaseModel):
    access_token = FixedCharField(max_length=36, verbose_name='用户授权令牌', null=False)
    aliId = IntegerField(null=False, verbose_name='阿里巴巴集团统一的id')
    refresh_token = FixedCharField(max_length=36, null=False, verbose_name='用户刷新令牌')
    resource_owner = FixedCharField(max_length=25, null=False, verbose_name='登录id')
    refresh_token_timeout = FixedCharField(null=False, max_length=22, verbose_name='用户刷新令牌到期时间')
    # 主键
    memberId = FixedCharField(max_length=22, null=False, primary_key=True, verbose_name='会员接口id')
    addressLocation = FixedCharField(max_length=35, verbose_name='定位地址', null=False)
    buyKeywords = FixedCharField(max_length=25, verbose_name='购买关键字', null=False)
    buyRate = SmallIntegerField(null=False, verbose_name='购买指数')
    categoryId = SmallIntegerField(null=False, verbose_name='类目ID')
    categoryName = FixedCharField(null=False, max_length=15, verbose_name='类目名称')
    companyName = FixedCharField(null=False, max_length=20, verbose_name='公司名称')
    createDate = FixedCharField(null=False, max_length=22, verbose_name='创建账号时间')
    domainInPlatforms = FixedCharField(null=False, max_length=255, verbose_name='账号下店铺')
    homepageUrl = FixedCharField(null=False, max_length=30, verbose_name='首页url')
    memberBizType = FixedCharField(null=False, max_length=15, verbose_name='账号业务类型')
    phoneNo = FixedCharField(null=False, max_length=19, verbose_name='联系电话')
    product = FixedCharField(null=False, max_length=100, verbose_name='产品')
    saleKeywords = FixedCharField(null=False, max_length=36, verbose_name='销售关键词')
    sellerName = FixedCharField(null=False, max_length=15, verbose_name='卖家姓名')
    shopUrl = FixedCharField(null=False, max_length=60, verbose_name='店铺url')
    supplierName = FixedCharField(null=False, max_length=20, verbose_name='供应商名字')
    tpYear = SmallIntegerField(null=False, verbose_name='淘宝年龄')
    trustScore = SmallIntegerField(null=False, verbose_name='诚信分数')
    update_time = DateTimeField(null=False, verbose_name='更新时间')
