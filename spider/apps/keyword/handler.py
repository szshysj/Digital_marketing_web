from Digital_marketing.handler import BaseHandler
from BaseRequest.GetOfferKeyword import GetOfferKeyword
from BaseRequest.GetOfferKeywordCpc import GetOfferKeywordCpc
from BaseRequest.AddOfferKeyword import AddOfferKeyword
from BaseRequest.GetAdgroupKeywordList import GetAdgroupKeywordList
from apps.keyword.forms import GetOfferKeywordForm, GetOfferKeywordCpcForm, AddOfferKeywordForm, \
    GetAdgroupKeywordListForm
from apps.user.models import Offer_Keyword, Offer_Keyword_7days
from datetime import datetime

from ujson import loads


class AddKeywordToMysqlHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))

        # 遍历每一条数据
        for data in param['keyword_list']:
            try:
                # 能查到数据
                await self.application.objects.get(
                    Offer_Keyword.select(Offer_Keyword.keyword).where(Offer_Keyword.keyword == data[0]))

                # 开启事务, update数据, 失败自动rollback
                async with self.application.objects.atomic():
                    await self.application.objects.execute(Offer_Keyword.update(
                        recommendTags=data[1],
                        countBuyer=data[2],
                        leftAvgClick7days=round(data[3], 2),
                        leftAvgPV7days=round(data[4], 2),
                        searchAvg7days=data[5],
                        update_time=datetime.now()
                    ).where(Offer_Keyword.keyword == data[0]))

            except Offer_Keyword.DoesNotExist:  # 找不到数据, 作insert操作
                # 保存数据到 "唯一" 的库
                async with self.application.objects.atomic():
                    await self.application.objects.create(Offer_Keyword,
                                                          keyword=data[0],
                                                          recommendTags=data[1],
                                                          countBuyer=data[2],
                                                          leftAvgClick7days=round(data[3], 2),
                                                          leftAvgPV7days=round(data[4], 2),
                                                          searchAvg7days=data[5],
                                                          update_time=datetime.now())

            # 保存数据到 '历史' 库
            async with self.application.objects.atomic():
                await self.application.objects.create(Offer_Keyword_7days,
                                                      keyword=data[0],
                                                      recommendTags=data[1],
                                                      countBuyer=data[2],
                                                      leftAvgClick7days=round(data[3], 2),
                                                      leftAvgPV7days=round(data[4], 2),
                                                      searchAvg7days=data[5],
                                                      update_time=datetime.now())

        await self.finish('finish')


class GetAdgroupKeywordListHandler(BaseHandler):

    async def get(self):

        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}
        form = GetAdgroupKeywordListForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await GetAdgroupKeywordList.get(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class AddOfferKeywordHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = AddOfferKeywordForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await AddOfferKeyword.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetOfferKeywordCpcHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = GetOfferKeywordCpcForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await GetOfferKeywordCpc.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetOfferKeywordHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}
        form = GetOfferKeywordForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await GetOfferKeyword.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
