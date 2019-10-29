#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from apps.offer.forms import GetOfferForm
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi
from time import localtime, strftime
from os.path import join

from tornado.httpclient import HTTPClientError
from aiofiles import open


class GetOfferHandler(RedisHandler):

    async def write_log(self, *args):
        async with open(join(self.application.settings['log_path'], 'get_offer.log'), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data = {}

        dict = {
            'page_num': self.get_argument('page_num', None)
        }

        form = GetOfferForm.from_json(dict)

        if form.validate():

            api = BaseApi(self.current_user.access_token)
            param = {'pageNo': form.page_num.data, 'pageSize': 20, 'needDetail': 'false', 'needFreight': 'false'}

            try:
                rp = await api.send_request(api_url='1/com.alibaba.product/alibaba.product.list.get', param=param,
                                            timestamp=False)
            except HTTPClientError as e:
                await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                     str(e.response.body.decode('utf8')), '获取商品列表失败')
                self.set_status(404)
                re_data['code'] = 1005,
                re_data['message'] = '获取商品列表失败'
                return await self.finish(re_data)
            else:
                return await self.finish(rp)

        else:
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            await self.finish(re_data)
