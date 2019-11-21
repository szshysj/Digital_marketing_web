from Digital_marketing.handler import BaseHandler
from Digital_marketing.forms import BaseForm
from apps.campaign.forms import AddCampaignForm
from BaseRequest.AddCampaign import AddCampaign
from BaseRequest.GetAllCampaign import GetAllCampaign

from ujson import loads


class GetAllCampaignHandler(BaseHandler):

    async def get(self):
        param = loads(self.request.body.decode('utf8'))
        form = BaseForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetAllCampaign.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class AddCampaignHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = AddCampaignForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await AddCampaign.post(form, self.application.session)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)