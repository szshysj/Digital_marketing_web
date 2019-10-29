#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 20:48
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import RedisHandler
from apps.authorization.models import User
from Request_Base_Api.BaseApi import BaseApi
from datetime import datetime
from time import strftime, localtime
from os.path import join

from jwt import encode as jwt_encode
from ujson import dumps, loads
from tornado.httpclient import AsyncHTTPClient, HTTPClientError
from aiofiles import open


class GetCodeHandler(RedisHandler):

    async def write_log(self, *args):

        async with open(join(self.application.settings['log_path'], 'authorization.log'), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    async def get_token(self, code):

        url = f'https://gw.open.1688.com/openapi/http/1/system.oauth2/getToken/{self.application.settings["app_key"]}'

        body = 'grant_type=authorization_code' + '&'
        body += 'need_refresh_token=true' + '&'
        body += f'client_id={self.application.settings["app_key"]}' + '&'
        body += f'client_secret={self.application.settings["app_secret"]}' + '&'
        body += f'redirect_uri={self.application.settings["app_callback_url"]}/get_code/' + '&'
        body += f'code={code}'

        rp = await AsyncHTTPClient().fetch(url, method='POST', body=body)

        return loads(rp.body.decode('utf8'))

    @staticmethod
    async def get_account_message(api):

        rp_twice = await api.send_request(api_url='1/com.alibaba.account/alibaba.account.basic', timestamp=False)

        return loads(rp_twice)

    def get_jwt(self, rp):

        payload = {
            'id': rp['memberId'],
            'exp': datetime.utcnow()  # 必须要用utc
        }

        token = jwt_encode(payload, self.application.settings['secret_key'], algorithm='HS256')

        return token.decode('utf8')

    async def write_db(self, rp, rp_twice):

        try:
            user = await self.application.objects.get(User, memberId=rp['memberId'])
            # 账号存在, 更新
            user.access_token = rp['access_token']
            user.refresh_token = rp['refresh_token']
            user.addressLocation = rp_twice['result']['addressLocation']
            user.buyKeywords = rp_twice['result'].get('buyKeywords', '')
            user.buyRate = rp_twice['result'].get('buyRate', '')
            user.categoryId = rp_twice['result']['categoryId']
            user.categoryName = rp_twice['result']['categoryName']
            user.companyName = rp_twice['result'].get('companyName', '')
            user.domainInPlatforms = rp_twice['result'].get('domainInPlatforms', '')
            user.homepageUrl = rp_twice['result'].get('homepageUrl', '')
            user.memberBizType = rp_twice['result'].get('memberBizType', '')
            user.phoneNo = rp_twice['result']['phoneNo']
            user.product = rp_twice['result']['product']
            user.saleKeywords = rp_twice['result'].get('saleKeywords', '')
            user.sellerName = rp_twice['result']['sellerName']
            user.shopUrl = rp_twice['result']['shopUrl']
            user.supplierName = rp_twice['result'].get('supplierName', '')
            user.tpYear = rp_twice['result']['tpYear']
            user.trustScore = rp_twice['result']['trustScore']
            user.update_time = datetime.now()
            await self.application.objects.update(user)

        except User.DoesNotExist:  # 账号不存在, 新增

            await self.application.objects.create(User,
                                                  access_token=rp['access_token'],
                                                  aliId=rp['aliId'],
                                                  refresh_token=rp['refresh_token'],
                                                  resource_owner=rp['resource_owner'],
                                                  refresh_token_timeout=rp['refresh_token_timeout'],
                                                  memberId=rp['memberId'],
                                                  addressLocation=rp_twice['result']['addressLocation'],
                                                  buyKeywords=rp_twice['result'].get('buyKeywords', ''),
                                                  buyRate=rp_twice['result'].get('buyRate', 0),
                                                  categoryId=rp_twice['result']['categoryId'],
                                                  categoryName=rp_twice['result']['categoryName'],
                                                  companyName=rp_twice['result'].get('companyName', ''),
                                                  createDate=rp_twice['result']['createDate'],
                                                  domainInPlatforms=rp_twice['result'].get('domainInPlatforms', ''),
                                                  homepageUrl=rp_twice['result'].get('homepageUrl', ''),
                                                  memberBizType=rp_twice['result'].get('memberBizType', ''),
                                                  phoneNo=rp_twice['result']['phoneNo'],
                                                  product=rp_twice['result']['product'],
                                                  saleKeywords=rp_twice['result'].get('saleKeywords', ''),
                                                  sellerName=rp_twice['result']['sellerName'],
                                                  shopUrl=rp_twice['result']['shopUrl'],
                                                  supplierName=rp_twice['result'].get('supplierName', ''),
                                                  tpYear=rp_twice['result']['tpYear'],
                                                  trustScore=rp_twice['result']['trustScore'],
                                                  update_time=datetime.now())

    async def get(self):

        re_data = {}

        code = self.get_argument('code', None)

        # 调用 get_token接口
        try:
            rp = await self.get_token(code)
        except HTTPClientError as e:
            await self.write_log(str(code), str(e), str(e.response.body.decode('utf8')), '调用get_token接口失败')
            self.set_status(404)
            re_data['code'] = 1000,
            re_data['message'] = '调用get_token接口失败'
            return await self.finish(re_data)

        # 自定义请求类
        api = BaseApi(access_token=rp['access_token'])

        # 调用 获取授权账户信息接口
        try:
            rp_twice = await self.get_account_message(api)
        except HTTPClientError as e:
            await self.write_log(str(rp), str(e), str(e.response.body.decode('utf8')), '获取账户信息失败')
            self.set_status(404)
            re_data['code'] = 1001,
            re_data['message'] = '获取账户信息失败'
            return await self.finish(re_data)

        # 账号信息入库
        try:
            await self.write_db(rp, rp_twice)
        except Exception as e:
            await self.write_log(str(rp), str(rp_twice), str(e), '同步账号信息失败')
            self.set_status(404)
            re_data['code'] = 1002,
            re_data['message'] = '同步账号信息失败'
            return await self.finish(re_data)

        # 生成Json Web Token
        re_data['JSESSION'] = self.get_jwt(rp)

        await self.finish(dumps(re_data))
