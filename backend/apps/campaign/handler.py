#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from apps.campaign.forms import AddCampaignForm, UpdateCampaignStatusForm, UpdateCampaignForm
from apps.authorization.models import User_campaign
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi
from time import localtime, strftime
from os.path import join
from re import match
from playhouse.shortcuts import model_to_dict

from ujson import loads
from tornado.httpclient import HTTPClientError
from aiofiles import open


class UpdataCampaignStatusHandler(BaseHandler):

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


class UpdateCampaignHandler(BaseHandler):

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


class GetCampaignHandler(BaseHandler):

    @authenticated_async
    async def get(self, *args, **kwargs):

        # 获取库里的数据
        campaign = await self.application.objects.execute(
            User_campaign.select(
                User_campaign.campaignId,
                User_campaign.modifiedTime
            ).where(
                User_campaign.memberId == self.current_user.memberId))

        # 库里没有数据后面就没有意义了, 因为必须以 库里数据和线上 共有的数据为准
        if not campaign:
            return await self.finish({'result': []})

        api = BaseApi(self.current_user.access_token)

        # 获取线上所有推广计划
        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.list')
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(e.response.body.decode('utf8')),
                                 '获取推广计划失败',
                                 filename='get_campaign')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))
        else:
            resp = loads(resp)

            # 线上没有任何推广计划, 说明库里的计划被用户手动删除了
            if not resp['campaigns']:
                return await self.finish({'result': [], 'msg': '线上没有任何推广计划'})

            # 库里数据格式化
            list_result = []
            for result in campaign:
                list_temp = []
                result = model_to_dict(result)
                list_temp.append(int(result['campaignId']))
                list_temp.append(str(result['modifiedTime']))
                list_result.append(tuple(list_temp))

            # 对线上数据进行格式化
            list_result_one = []
            for result in resp['campaigns']:
                list_temp = []
                list_temp.append(result['campaignId'])
                list_temp.append(result['modifiedTime'])
                list_result_one.append(tuple(list_temp))

            # 找出共有的数据, 找出没有被用户污染过的数据(用户手动修改, 使用其他工具修改本工具计划等), 确保是我们的数据
            result = set(list_result) & set(list_result_one)

            if not result:
                # 数据被污染过, 过滤掉
                return await self.finish({'result': [], 'msg': '没有符合我们的数据'})

            list_tmp = []
            for tmp in result:
                for tmp_2 in resp['campaigns']:
                    if tmp[0] == tmp_2['campaignId']:
                        list_tmp.append(tmp_2)
                        break

            await self.finish({'result': list_tmp})


class AddCampaignHandler(BaseHandler):

    @authenticated_async
    async def post(self, *args, **kwargs):

        param = self.request.body.decode('utf8')

        form = AddCampaignForm.from_json(loads(param))

        if not form.validate():
            return await self.finish(self.error_handle(form))

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
                                 str(param),
                                 str(e.response.body.decode('utf8')),
                                 '创建推广计划失败',
                                 filename='post_campaign')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))
        else:

            result = loads(rp)  # 解析成功数据

            try:
                await self.application.objects.create(User_campaign,
                                                      memberId=self.current_user.memberId,
                                                      campaignId=result['campaign']['campaignId'],
                                                      title=result['campaign']['title'],
                                                      budget=result['campaign']['budget'],
                                                      promoteArea=result['campaign']['promoteArea'],
                                                      schedule=form.schedule.data,
                                                      onlineStatus=result['campaign']['onlineStatus'],
                                                      settleStatus=result['campaign']['settleStatus'],
                                                      cositeFlag=result['campaign']['cositeFlag'],
                                                      createTime=result['campaign']['createTime'],
                                                      modifiedTime=result['campaign']['modifiedTime'])
            except Exception as e:
                await self.write_log(str(self.current_user.memberId),
                                     str(result['campaign']['campaignId']),
                                     str(result['campaign']['title']),
                                     str(result['campaign']['budget']),
                                     str(result['campaign']['promoteArea']),
                                     str(form.schedule.data),
                                     str(result['campaign']['onlineStatus']),
                                     str(result['campaign']['settleStatus']),
                                     str(result['campaign']['cositeFlag']),
                                     str(result['campaign']['createTime']),
                                     str(result['campaign']['modifiedTime']),
                                     str(e),
                                     '创建推广计划sql记录失败',
                                     filename='post_campaign')
                self.set_status(404)
                return await self.finish({'result': 'sql提交错误'})
            else:
                await self.finish(rp)
