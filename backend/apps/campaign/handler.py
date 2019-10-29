#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from apps.campaign.forms import AddCampaignForm, UpdateCampaignStatusForm, UpdateCampaignForm
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi
from time import localtime, strftime
from os.path import join
from re import match

from ujson import loads
from tornado.httpclient import HTTPClientError
from aiofiles import open


class DeleteCampaignHandler(RedisHandler):

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = loads(self.request.body.decode('utf8'))

        if not isinstance(param['campaignIdList'], list):
            re_data['message'] = '参数必须是列表'
            return await self.finish(re_data)

        api = BaseApi(access_token=self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.delete', param=param)
        except HTTPClientError as e:
            print(e.code)
            print(e.message)
            print(e.args)
            return await self.finish(e.response.body.decode('utf8'))

        await self.finish(resp)


class UpdataCampaignStatusHandler(RedisHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = loads(self.request.body.decode('utf8'))
        form = UpdateCampaignStatusForm.from_json(param)

        if form.validate():
            param = {
                'campaignId': form.campaignId.data,
                'onlineStatus': form.status.data
            }
            api = BaseApi(access_token=self.current_user.access_token)

            try:
                resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.update', param=param)
            except HTTPClientError as e:
                await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                     str(e.response.body.decode('utf8')), '暂停推广计划失败',
                                     filename='update_campaign_status.log')
                self.set_status(404)
                re_data['code'] = 1011,
                re_data['message'] = '暂停推广计划失败'
                return await self.finish(re_data)
            else:
                await self.finish(resp)

        else:
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            await self.finish(re_data)


class UpdateCampaignHandler(RedisHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @staticmethod
    def get_schedule(type_num):

        # 全天 7*24小时
        # 热门时间段  上午10点到12点   下午3点到6点    晚上9点到11点
        # 闲时 晚上9点到早上6点

        schedule_dict = {
            # 7*24 全天
            1: '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111111111111111111111111111',
            # 7*24 热门
            2: '000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000011000111000110',
            # 7*24 闲时
            3: '111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111111111000000000000000111',
            # 工作日 全天
            4: '000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111000000000000000000000000',
            # 工作日 热门
            5: '000000000000000000000000000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000000000000000000',
            # 工作日 闲时
            6: '000000000000000000000000111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111000000000000000000000000',
            # 休息日 全天
            7: '111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111111111111111111111',
            # 休息日 热门
            8: '000000000011000111000110000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000000000000011000111000110',
            # 休息日 闲时
            9: '111111000000000000000111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111000000000000000111'
        }

        return schedule_dict[type_num]

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode('utf8')
        param = loads(param)
        form = UpdateCampaignForm.from_json(param)

        if form.validate():
            param = {
                'campaignId': form.campaignId.data,
                'budget': form.budget.data,
                'promoteArea': form.promoteArea.data,
                'schedule': self.get_schedule(form.schedule.data),
                'cositeFlag': form.cositeFlag.data
            }

            api = BaseApi(access_token=self.current_user.access_token)

            try:
                resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.update', param=param)
            except HTTPClientError as e:
                await self.write_log(str(self.current_user.access_token), str(param), str(e),
                                     str(e.response.body.decode('utf8')), '修改推广计划失败',
                                     filename='update_campaign.log')
                self.set_status(404)
                re_data['code'] = 1012,
                re_data['message'] = '修改推广计划失败'
                return await self.finish(re_data)
            else:
                await self.finish(resp)

        else:
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            await self.finish(re_data)


class AddCampaignHandler(RedisHandler):

    @staticmethod
    def re_match(title):
        try:
            match('.*(-財源廣進-\\d{14})', title['title']).group(1)
            return title
        except AttributeError:
            return False

    @staticmethod
    def get_schedule(type_num):
        """
        全天 7*24小时
        热门时间段  上午10点到12点   下午3点到6点    晚上9点到11点
        闲时 晚上9点到早上6点

        :param type_num: 时段类型
        :return: 具体的值
        """

        schedule_dict = {
            # 7*24 全天
            1: '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111111111111111111111111111',
            # 7*24 热门
            2: '000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000011000111000110',
            # 7*24 闲时
            3: '111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111111111000000000000000111',
            # 工作日 全天
            4: '000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111000000000000000000000000',
            # 工作日 热门
            5: '000000000000000000000000000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000000000000000000',
            # 工作日 闲时
            6: '000000000000000000000000111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111000000000000000000000000',
            # 休息日 全天
            7: '111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111111111111111111111',
            # 休息日 热门
            8: '000000000011000111000110000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000000000000011000111000110',
            # 休息日 闲时
            9: '111111000000000000000111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111000000000000000111'
        }

        return schedule_dict[type_num]

    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data = {}

        api = BaseApi(self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.list')
        except HTTPClientError as e:
            self.set_status(404)
            await self.write_log(str(self.current_user.access_token), str(e),
                                 str(e.response.body.decode('utf8')), '获取所有推广计划失败')
            re_data['code'] = 1006,
            re_data['message'] = '获取所有推广计划失败'
            return await self.finish(re_data)

        # 找出属于本app的计划
        # resp = loads(resp)
        # result = list(filter(self.re_match, resp['campaigns']))

        # re_data['result'] = result

        await self.finish(resp)

    @authenticated_async
    async def post(self, *args, **kwargs):

        param = self.request.body.decode('utf8')

        form = AddCampaignForm.from_json(loads(param))

        if not form.validate():
            re_data = {}
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            return await self.finish(re_data)

        api = BaseApi(self.current_user.access_token)

        param = {
            'title': form.campaign_name.data + f'-財源廣進-{strftime("%Y%m%d%H%M%S", localtime())}',
            'budget': form.budget.data,
            'onlineStatus': '1',
            'schedule': self.get_schedule(form.schedule.data),
            'cositeFlag': form.cositeFlag.data,
            'promoteArea': form.promoteArea.data
        }

        try:
            rp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.add', param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param), str(e.response.body.decode('utf8')),
                                 str(e.response.body.decode('utf8')),
                                 '创建推广计划失败',
                                 filename='post_campaign.log')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))
        else:
            await self.finish(rp)
