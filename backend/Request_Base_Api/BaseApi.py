#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/5 15:49
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from hashlib import sha1
from time import time
from Digital_marketing.settings import settings
from hmac import new

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import url_escape


class BaseApi:

    def __init__(self, access_token):
        """
        :param access_token: 用户授权令牌
        """

        # 最终请求路径
        self._request_url = 'http://gw.open.1688.com/openapi/'
        # 用户授权令牌
        self._access_token = access_token

    @staticmethod
    def urlencode(param):
        return url_escape(str(param), plus=False)

    def _get_sign(self, api_url, param, timestamp):

        # 带上access_token
        param['access_token'] = self._access_token

        # 是否需要带上时间戳
        if timestamp:
            param['_aop_timestamp'] = str(int(time()) * 1000)
        try:  # 删除上次携带的参数
            param.pop('_aop_signature')
        except KeyError:
            pass

        # 对param进行排序
        param_list = []
        [param_list.append(f'{k}{y}') for k, y in param.items()]
        param_list.sort()

        # 构造请求url, 此值需要return
        request_url = 'param2/' + api_url + '/' + settings['app_key']

        # 构造签名因子
        sign_str = request_url + ''.join(param_list)
        s = bytes(sign_str.encode('utf-8'))
        sha = new(bytes(settings['app_secret'].encode('utf-8')), None, sha1)
        sha.update(s)
        param['_aop_signature'] = sha.hexdigest().upper()

        # 返回url和参数字典
        return self._request_url + request_url, param

    async def send_request(self, api_url, param=None, timestamp=True, method='GET'):

        # 判断是否传进参数
        if not param:
            param = {}

        # 进行签名, 获得请求body体
        url, body = self._get_sign(api_url, param, timestamp)

        # 拼接url参数部分
        param_str = ''
        for k, y in body.items():
            param_str += f'{k}={self.urlencode(y)}&'

        # 生成url
        url += '?' + param_str[:-1]

        if method == 'GET':
            resp = await AsyncHTTPClient().fetch(url)
        else:
            resp = await AsyncHTTPClient().fetch(url, method='POST')

        return resp.body.decode('utf8')
