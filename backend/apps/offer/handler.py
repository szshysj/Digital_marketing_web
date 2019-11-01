#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 22:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from tools.decorator import authenticated_async
from Request_Base_Api.BaseApi import BaseApi

from tornado.httpclient import HTTPClientError
from ujson import loads


class GetOfferHandler(BaseHandler):

    @authenticated_async
    async def get(self, campaign_id, page_num, *args, **kwargs):

        api = BaseApi(self.current_user.access_token)

        param = {'pageNo': page_num, 'pageSize': 20, 'needDetail': 'false', 'needFreight': 'false'}

        # 获得卖家商品列表某一页
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
            # 解析数据
            rp = loads(rp)

            # 如果是空, 继续执行没有意义了
            if not rp['result']['pageResult']['resultList']:
                return await self.finish({'result': [], 'msg': '用户供应商品列表为空'})

            # 获取数据的所有商品id
            list_1 = []  # 商品id列表
            [list_1.append(result['productID']) for result in rp['result']['pageResult']['resultList']]

        # =======================================================================================================

        # 商品id列表
        list_2 = []

        # 获取指定推广计划下的所有所有推广单元
        param = {
            'campaignId': campaign_id,
            'pageNo': 1,
            'pageSize': 200,
        }

        num = 1  # 固定请求最大次数
        while num <= 5:
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
                # 解析数据
                resp = loads(resp)

                # 第一次请求或后续请求没有结果, 退出循环
                if not resp['adgroups']:
                    break

                # 获取数据的所有商品id
                [list_2.append(result['offerId']) for result in resp['adgroups']]

                # 获得单元总数
                total_num = resp['totalRow']

                # 单元总数大于等于200, value肯定大于等于1.0
                # 单元数小于200200, value肯定小于1.0
                value = total_num / 200

                # 请求一次就好, 数据要么小于200条, 要么正好等于200条
                if value <= 1:
                    break

                param['pageNo'] += 1
                num += 1

        # 只有一种情况, 当前推广计划下推广单元列表是空的, 直接返回全部商品
        if not list_2:
            return await self.finish({'result': rp, 'repeat_offer': []})

        result = list(set(list_1) & set(list_2))

        # 请求的当前商品列表 里 没有在投的推广单元
        if not result:
            return await self.finish({'result': rp, 'repeat_offer': []})

        # 当前商品列表里, 有在投的推广单元
        await self.finish({'result': rp, 'repeat_offer': result})
