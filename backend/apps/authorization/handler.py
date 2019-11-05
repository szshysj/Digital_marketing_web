#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 20:48
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.handler import BaseHandler
from Request_Base_Api.get_token import get_token
from Request_Base_Api.get_account_info import GetAccountInfo
from apps.authorization.models import User
from datetime import datetime

from jwt import encode as jwt_encode


class GetCodeHandler(BaseHandler):

    def get_jwt(self, text_):

        payload = {
            'id': text_['memberId'],
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

        code = self.get_argument('code', None)

        if not code:
            self.set_status(404)
            return await self.finish({'error_message': 'code为空'})

        # 进行授权认证
        status_code, text = await get_token(code, self.application.session, self.application.settings)
        if status_code != 200:
            await self.write_log(str(text), '调用get_token接口失败', filename='authorization')
            self.set_status(401)
            return await self.finish({'error_message': '调用get_token接口失败'})

        # 调用 获取授权账户信息api
        api = GetAccountInfo(access_token=text['access_token'])
        status_code, text_2 = await api.send_request(self.application.session, timestamp=False)
        if status_code != 200:
            await self.write_log(str(text), '获取账户信息失败', filename='authorization')
            self.set_status(404)
            return await self.finish({'error_message': '获取账户信息失败'})

        # 获得账号信息, 把信息写入到数据库
        try:
            await self.write_db(text, text_2)
        except Exception as e:
            await self.write_log(str(text), str(text_2), str(e), '同步账号信息失败', filename='authorization')
            self.set_status(404)
            return await self.finish({'error_message': '同步账号信息失败'})

        # 生成Json Web Token
        await self.finish({'JSESSION': self.get_jwt(text)})
