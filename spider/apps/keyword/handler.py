from Digital_marketing.handler import BaseHandler
from BaseRequest.GetOfferKeyword import GetOfferKeyword
from BaseRequest.GetOfferKeywordCpc import GetOfferKeywordCpc
from BaseRequest.AddOfferKeyword import AddOfferKeyword
from apps.keyword.forms import GetOfferKeywordForm, GetOfferKeywordCpcForm, AddOfferKeywordForm

from ujson import loads


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
        param = loads(self.request.body.decode('utf8'))
        form = GetOfferKeywordForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await GetOfferKeyword.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
