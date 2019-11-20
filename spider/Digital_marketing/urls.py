#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 19:50
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from apps.user.urls import urls_pattern as user_urls
from apps.campaign.urls import urls_pattern as campaign_urls
from apps.offer.urls import urls_pattern as offer_urls
from apps.adgroup.urls import urls_pattern as adgroup_urls
from apps.keyword.urls import urls_pattern as keyword_urls

urlspatten = []

urlspatten += user_urls
urlspatten += campaign_urls
urlspatten += offer_urls
urlspatten += adgroup_urls
urlspatten += keyword_urls
