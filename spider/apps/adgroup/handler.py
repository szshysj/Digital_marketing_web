from Digital_marketing.handler import BaseHandler
from apps.adgroup.forms import AddAdgroupForm, GetCampaignAdgroupForm
from BaseRequest.AddAdgroup import AddAdgroup
from BaseRequest.GetCampaignAdgroup import GetCampaignAdgroup
from BaseRequest.GetCampaignAdgroupInfo import GetCampaignAdgroupInfo

from ujson import loads


class GetCampaignAdgroupInfoHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}

        resp = await GetCampaignAdgroupInfo.get(self.application.session, params)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetCampaignAdgroupHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}
        form = GetCampaignAdgroupForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetCampaignAdgroup.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class AddAdgroupHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = AddAdgroupForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await AddAdgroup.post(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
