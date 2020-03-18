#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 19:45
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.settings import database, settings
from apps.user.models import Account_Info, Offer_Keyword, Offer_Keyword_7days
from pprint import pprint as pp

from requests import get, post

"""======================================增================================================"""

"""
CREATE TABLE es_table (
  id BIGINT(20) UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY unique_id (id),
  client_name VARCHAR(32) NOT NULL,
  modification_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  insertion_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

def init():
    database.create_tables([Offer_Keyword, Offer_Keyword_7days])


def authorization(code):
    """
    code为app市场传过来的值
    """

    url = f'https://gw.open.1688.com/openapi/http/1/system.oauth2/getToken/{settings["app_key"]}'
    data = {
        'grant_type': 'authorization_code',
        'need_refresh_token': 'true',
        'client_id': settings["app_key"],
        'client_secret': settings['app_secret'],
        'redirect_uri': settings['app_callback_url'] + '/get_code/',
        'code': code
    }
    rp = post(url, data=data).json()
    pp(rp)


"""======================================删================================================"""

"""======================================查================================================"""

"""======================================改================================================"""

if __name__ == '__main__':
    """======================================增================================================"""
    init()  # 初始化数据库
    # authorization('asdasdasdsad324324sdfssd')  # 新用户授权
    """======================================删================================================"""
    """======================================查================================================"""
    """======================================改================================================"""
