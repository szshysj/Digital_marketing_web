#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/18 15:27
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from apps.keyword.forms import GetAdgroupKeywordHandler
from Request_Base_Api.BaseApi import BaseApi
from tools.decorator import authenticated_async
from os.path import join
from time import strftime, localtime
from ujson import loads

from tornado.httpclient import HTTPClientError
from aiofiles import open


class GetKeywordListByAdgroupHandle(RedisHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def get(self, adgroup_id, *args, **kwargs):

        form = GetAdgroupKeywordHandler.from_json({'adGroupId': adgroup_id})

        if not form.validate():
            re_data = {}
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            return await self.finish(re_data)

        api = BaseApi(access_token=self.current_user.access_token)

        param = {'adGroupId': form.adGroupId.data}

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.keyword.byadgroupid.list',
                                          param=param)
        except HTTPClientError as e:
            self.set_status(404)
            await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                 str(e.response.body.decode('utf8')), '根据adGroupId获取网销宝关键词列表失败',
                                 filename='get_keywordlist.log')
            return await self.finish(e.response.body.decode('utf8'))
        else:
            await self.finish(resp)


class GetKeywordHandler(RedisHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def get(self, adgroup_id, *args, **kwargs):
        re_data = {}
        param = {
            'adGroupId': adgroup_id
        }

        form = GetAdgroupKeywordHandler.from_json(param)

        if not form.validate():
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            return await self.finish(re_data)

        api = BaseApi(access_token=self.current_user.access_token)

        param = {'adGroupId': form.adGroupId.data, 'pageNo': 1, 'pageSize': 10}

        list_temp = []

        while param['pageNo'] <= 10:
            try:
                resp = await api.send_request('1/com.alibaba.p4p/alibaba.cnp4p.keyword.recommend.list', param=param)
            except HTTPClientError as e:
                await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                     str(e.response.body.decode('utf8')), '获取指定推广单元关键词失败',
                                     filename='get_keyword.log')
                self.set_status(404)
                re_data['code'] = 1009,
                re_data['message'] = '获取指定推广单元关键词失败'
                return await self.finish(re_data)
            else:
                result = loads(resp)
                list_temp += result['recommends']
                param['pageNo'] += 1

        # 过滤没有竞争指数的关键词
        list_ = list(filter(lambda x: 'pv' in x, list_temp))
        # 展示指数从大到小排序
        list_temp = sorted(list_, key=lambda x: x['qualityScore'], reverse=True)

        re_data['result'] = list_temp
        await self.finish(re_data)

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode('utf8')

        param = loads(param)

        param = {
            'adGroupId': param['adGroupId'],
            'keywords': param['keywords']
        }

        api = BaseApi(access_token=self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.keyword.add', param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                 str(e.response.body.decode('utf8')), '添加网销宝关键词失败',
                                 filename='post_keyword.log')
            self.set_status(404)
            re_data['code'] = 1010,
            re_data['message'] = '添加网销宝关键词失败'
            return await self.finish(re_data)
        else:
            await self.finish(resp)
