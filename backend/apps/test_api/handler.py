#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/29 11:04
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler


class TestHandler(RedisHandler):

    async def get(self):
        await self.finish({'result': '成功'})
