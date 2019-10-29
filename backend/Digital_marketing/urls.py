#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 19:50
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from apps.authorization.urls import urlpatten as authorization_urls
from apps.area.urls import urlpatten as area_urls
from apps.campaign.urls import urlpatten as campaign_urls
from apps.offer.urls import urlpatten as offer_urls
from apps.adgroup.urls import urlpatten as adgroup_urls
from apps.keyword.urls import urlpatten as keyword_urls
from apps.test_api.urls import urlpatten as test_urls

urlspatten = []

urlspatten += authorization_urls
urlspatten += area_urls
urlspatten += campaign_urls
urlspatten += offer_urls
urlspatten += adgroup_urls
urlspatten += keyword_urls
urlspatten += test_urls