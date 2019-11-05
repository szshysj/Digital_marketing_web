#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 13:48
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Request_Base_Api.BaseApi import BaseApi


class GetAccountInfo(BaseApi):

    def __init__(self, access_token):
        super().__init__(access_token)
        self._api_url = '1/com.alibaba.account/alibaba.account.basic'
