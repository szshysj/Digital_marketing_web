#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 23:44
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from re import match
from Request_Base_Api.BaseApi import BaseApi
from requests import post, get
from Digital_marketing.settings import settings, token
from pprint import pprint as pp
from asyncio import run
from time import time, perf_counter

from ujson import dumps, loads


# 推广计划id   817907510
# 推广单元      386201818
# 商品id       600095550215


def post_campaign():
    param = {
        'campaign_name': '测试开发',
        'budget': '60',
        'promoteArea': '2610,10000',
        'schedule': '1',
        'cositeFlag': '1'
    }
    rp = post(url + '/post/campaign/', json=param, headers=headers)
    print(rp.text)


def post_adgroup():
    param = {
        'campaignId': 817907510,
        'bidPrice': 1,
        'offerId': 599945740925
    }
    rp = post(url + '/post/adgroup/', json=param, headers=headers).json()
    pp(rp)


def get_adgroup_keyword():
    rp = get(url + '/get/keyword/386201818/', headers=headers).json()
    pp(rp)


def post_keyword():
    data = {
        'adGroupId': 386201818,
        'keywords': [
            {'keyword': '姜糖', 'bidPrice': 0.5}
        ]
    }
    rp = post(url + '/post/keyword/', json=data, headers=headers).json()
    pp(rp)


def get_campaign():
    rp = get(url + '/get/campaign/', headers=headers).json()
    pp(rp)


def update_campaign_status():
    data = {
        'campaignId': '817038052',
        'status': '1'
    }
    rp = post(url + '/update/campaign/status/', headers=headers, json=data).json()
    print(rp)


def update_campaign():
    data = {
        'campaignId': 816865260,
        'budget': 70,
        'promoteArea': '4846,4853,10000,4858',
        'schedule': 6,
        'cositeFlag': '0'
    }
    rp = post(url + '/update/campaign/', json=data, headers=headers)
    print(rp.text)


def get_area():
    rp = get(url + '/get/area/', headers=headers).json()
    print(rp)


# 获取阿里指数新版
def get_alibaba_index_spider():
    """
    永远是最近6天
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    cookie = {
        'cookie2': '18a375d98a1be4d7b4389f84a2b127a6',
        'sg': '287'
    }
    data = {
        'query': "{\n  hot {\n    cate(areaId: 110000, dateType: \"recent7\", period: [\"20191022\", \"20191022\"], type: \"buyer\") "
                 "{\n      areaId\n      areaName\n      cateId\n      cateName\n      tradeIndex\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    rp = post('https://alizs.taobao.com/api/oneql', cookies=cookie, json=data, verify=False, headers=headers, timeout=5)
    try:
        pp(rp.json())
    except ValueError as e:
        print(e)
        print(rp.text)


def delete_campaign():
    data = {
        'campaignIdList': [816865260, 817779155]
    }
    rp = post(url + '/delete/campaign/', headers=headers, json=data)
    print(rp.text)


def get_adgroup():
    rp = get(url + '/get/adgroup/817907510/1/', headers=headers).json()
    pp(rp)


def update_adgroup_status():
    data = {
        'campaignId': '816865260',
        'adGroupId': '382985732',
        'onlineState': '1',
    }
    rp = post(url + '/update/adgroup/status/', headers=headers, json=data)
    print(rp.text)


def delete_adgroup():
    data = {
        'adGroupId': '382985732'
    }
    rp = post(url + '/delete/adgroup/', headers=headers, json=data)
    print(rp.text)


def get_keyword_list():
    rp = get(url + '/get/keywordlist/386223913/', headers=headers).json()
    pp(rp)


def get_offer():
    rp = get(url + '/get/offer/816508540/1/', headers=headers).json()
    pp(rp)


if __name__ == '__main__':
    headers = {'JSESSION': token['token']}
    url = settings['app_callback_url']

    # 增
    # post_campaign()
    # post_adgroup()
    # post_keyword()
    # 删
    # delete_campaign()
    # delete_adgroup()
    # 查
    # get_offer()
    # get_adgroup_keyword()
    # get_campaign()
    get_area()
    # get_adgroup()
    # get_keyword_list()
    # 改
    # update_campaign_status()
    # update_campaign()
    # update_adgroup_status()
