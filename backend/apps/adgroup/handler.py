#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/16 23:41
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from apps.adgroup.forms import CreateAdgroupForm, GetAdgroup, UpdateAdgroupStatusForm, DeleteAdgroupHandlerForm
from apps.authorization.models import User_campaign, User_adgroup
from tools.decorator import authenticated_async
from os.path import join
from time import strftime, localtime
from Request_Base_Api.BaseApi import BaseApi
from playhouse.shortcuts import model_to_dict

from ujson import loads
from aiofiles import open
from tornado.httpclient import HTTPClientError


class DeleteAdgroupHandler(BaseHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = loads(self.request.body.decode('utf8'))
        form = DeleteAdgroupHandlerForm.from_json(param)

        if not form.validate():
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            return await self.finish(re_data)

        param = {
            'adGroupId': form.adGroupId.data
        }

        api = BaseApi(access_token=self.current_user.access_token)

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.adgroup.delete', param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param),
                                 str(e),
                                 str(e.response.body.decode('utf8')),
                                 '删除推广单元失败',
                                 filename='delete_adgroup.log')
            return await self.finish(e.response.body.decode('utf8'))
        else:
            await self.finish(resp)


class UpdateAdgroupStatusHandler(BaseHandler):

    async def write_log(self, *args, filename):

        async with open(join(self.application.settings['log_path'], filename), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = loads(self.request.body.decode('utf8'))
        form = UpdateAdgroupStatusForm.from_json(param)

        if form.validate():
            param = {
                'campaignId': form.campaignId.data,
                'adGroupId': form.adGroupId.data,
                'onlineState': form.onlineState.data
            }

            api = BaseApi(access_token=self.current_user.access_token)

            try:
                resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.adgroup.update', param=param)
            except HTTPClientError as e:
                await self.write_log(str(self.current_user.access_token),
                                     str(param),
                                     str(e),
                                     str(e.response.body.decode('utf8')),
                                     '更新推广单元状态失败',
                                     filename='update_adgroup_status.log')
                self.set_status(404)
                return await self.finish(e.response.body.decode('utf8'))
            else:
                return await self.finish(resp)

        else:
            self.set_status(404)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
            await self.finish(re_data)


class GetAdgroupHandler(BaseHandler):

    @authenticated_async
    async def get(self, campaign_id, page_num, *args, **kwargs):

        form = GetAdgroup.from_json({'campaignId': campaign_id, 'pageNo': page_num})

        if not form.validate():
            return await self.finish(self.error_handle(form))

        api = BaseApi(access_token=self.current_user.access_token)

        param = {
            'campaignId': form.campaignId.data,
            'pageNo': form.pageNo.data,
            'pageSize': 200,
        }

        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.adgroup.bycampaignids.list',
                                          param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param),
                                 str(e.response.body.decode('utf8')),
                                 '获取推广计划下所有单元失败',
                                 filename='get_adgroup')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))

        else:
            return await self.finish(resp)


class CreateAdgroupHandler(BaseHandler):

    @authenticated_async
    async def post(self, *args, **kwargs):

        param = self.request.body.decode('utf8')

        form = CreateAdgroupForm.from_json(loads(param))

        if not form.validate():
            return await self.finish(self.error_handle(form))

        api = BaseApi(access_token=self.current_user.access_token)

        # 查询线上推广计划的修改时间
        param = {'campaignIdList': form.campaignId.data}
        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.campaign.list', param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param),
                                 str(e.response.body.decode('utf8')),
                                 '获取推广计划失败',
                                 filename='get_campaign')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))
        else:
            resp = loads(resp)

            if not resp['campaigns']:
                self.set_status(404)
                return await self.finish({"error_message": "此账号没有这条推广计划"})

            # 线上推广计划修改时间
            modifiedtime = resp['campaigns'][0]['modifiedTime']

        # =====================================================================================================

        # 查询线下推广计划修改时间
        try:
            result = await self.application.objects.get(
                User_campaign.select(
                    User_campaign.modifiedTime
                ).where(
                    User_campaign.campaignId == form.campaignId.data))
        except User_campaign.DoesNotExist:
            self.set_status(404)
            return await self.finish({'error_message': '此推广计划不属于本app'})
        else:
            # 将models字典化
            result = model_to_dict(result)
            # 将线上和线下的修改时间进行对比
            if modifiedtime != str(result['modifiedTime']):
                self.set_status(404)
                return await self.finish({"error_message": "此推广计划已被污染, 弃掉"})

        # =====================================================================================================

        # 开始创建推广单元
        param = {
            'campaignId': form.campaignId.data,
            'onlineState': 1,
            'bidPrice': form.bidPrice.data,
            'offerId': form.offerId.data
        }
        try:
            resp = await api.send_request(api_url='1/com.alibaba.p4p/alibaba.cnp4p.adgroup.add', param=param)
        except HTTPClientError as e:
            await self.write_log(str(self.current_user.access_token),
                                 str(param),
                                 str(e.response.body.decode('utf8')),
                                 '创建推广单元失败',
                                 filename='post_adgroup')
            self.set_status(404)
            return await self.finish(e.response.body.decode('utf8'))
        else:
            resp = loads(resp)
            resp = resp['adgroup']

            try:
                await self.application.objects.create(User_adgroup,
                                                      memberId=self.current_user.memberId,
                                                      auditState=resp['auditState'],
                                                      bidPrice=resp['bidPrice'],
                                                      campaignId=resp['campaignId'],
                                                      adGroupId=resp['adGroupId'],
                                                      createTime=resp['createTime'],
                                                      modifiedTime=resp['modifiedTime'],
                                                      offerId=resp['offerId'],
                                                      onlineState=resp['onlineState'],
                                                      title=resp['title'])
            except Exception as e:
                self.set_status(404)
                await self.write_log(str(self.current_user.access_token),
                                     str(resp),
                                     str(e),
                                     '增加推广单元失败',
                                     filename='write_adgroup')
                return await self.finish({'error_message': '增加推广单元失败'})
            await self.finish(resp)
