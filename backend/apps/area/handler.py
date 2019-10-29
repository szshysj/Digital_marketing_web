#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 23:28
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi
from os.path import join
from time import strftime, localtime

from tornado.httpclient import HTTPClientError
from aiofiles import open


class GetAreaHandler(RedisHandler):

    async def wtire_log(self, *args):

        async with open(join(self.application.settings['log_path'], 'area.log'), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def get(self, *args, **kwargs):

        re_data = {}

        api = BaseApi(self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.areaList')
        except HTTPClientError as e:
            self.set_status(404)
            await self.wtire_log(str(self.current_user.access_token), str(e),
                                 str(e.response.body.decode('utf8')), '请求可投放地域列表出错')
            re_data['code'] = 1003,
            re_data['message'] = '请求可投放地域列表出错'
            return await self.finish(re_data)

        await self.finish(resp)
