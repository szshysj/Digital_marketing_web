#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/29 11:04
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from apps.test_api.forms import Test1Form


class TestHandler(RedisHandler):

    async def get(self):
        await self.finish({'result': '成功'})


class Test1Handler(RedisHandler):
    async def get(self, *args, **kwargs):

        param = {
            'filed1': '1'
        }

        form = Test1Form.from_json(param)

        if not form.validate():
            re_data = {}
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            return await self.finish(re_data)

        await self.finish({'result': '陈宫'})
