#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/29 11:04
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from apps.test_api.forms import Test1Form


class TestHandler(BaseHandler):

    async def get(self):
        await self.finish({'result': '成功'})


class Test1Handler(BaseHandler):
    async def get(self, *args, **kwargs):
        await self.application.redis.set('kxx', '18645959590')
        bin_value = await self.application.redis.get('kxx')

        print(bin_value)
        print(bin_value.encode('utf8'))

        await self.finish({'result': bin_value})
