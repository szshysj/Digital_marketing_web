#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi

from tornado.httpclient import HTTPClientError


class GetOfferHandler(BaseHandler):

    @authenticated_async
    async def get(self, campaign_id, page_num, *args, **kwargs):

        api = BaseApi(self.current_user.access_token)
        param = {'pageNo': page_num, 'pageSize': 20, 'needDetail': 'false', 'needFreight': 'false'}

        # 获得商家商品列表
        try:
            rp = await api.send_request(api_url='1/com.alibaba.product/alibaba.product.list.get', param=param,
                                        timestamp=False)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param),
                                 str(e.response.body.decode('utf8')),
                                 '获取商家商品列表失败',
                                 filename='get_offer')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))

        else:
            await self.finish(rp)
