#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 23:28
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi

from tornado.httpclient import HTTPClientError


class GetAreaHandler(BaseHandler):

    @authenticated_async
    async def get(self, *args, **kwargs):

        api = BaseApi(self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.areaList')
        except HTTPClientError as e:
            self.set_status(404)
            await self.write_log(str(self.current_user.access_token),
                                 str(e.response.body.decode('utf8')),
                                 '请求可投放地域列表出错',
                                 filename='get_area')

            return await self.finish(e.response.body.decode('utf8'))

        else:
            await self.finish(resp)
