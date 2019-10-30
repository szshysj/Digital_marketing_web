#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:37
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from tornado.web import url
from apps.campaign.handler import AddCampaignHandler, UpdateCampaignHandler, UpdataCampaignStatusHandler, \
    GetCampaignHandler

urlpatten = [
    # 创建广告推广计划
    url('/post/campaign/', AddCampaignHandler),
    # 获取所有广告推广计划
    url('/get/campaign/', GetCampaignHandler),
    # 暂停广告推广计划
    # url('/update/campaign/status/', UpdataCampaignStatusHandler),
    # 修改广告推广计划
    # url('/update/campaign/', UpdateCampaignHandler)
]
