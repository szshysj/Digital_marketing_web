from Digital_marketing.handler import BaseHandler
from Digital_marketing.forms import BaseForm
from apps.campaign.forms import AddCampaignForm, GetCampaignInfoFrom, UpdateCampaignForm, DeleteCampaignForm, \
    CampaignReportForm
from BaseRequest.AddCampaign import AddCampaign
from BaseRequest.GetAllCampaign import GetAllCampaign
from BaseRequest.GetACampaignInfo import GetACampaignInfo
from BaseRequest.UpdateCampaign import UpdateCampaign
from BaseRequest.DeleteCampaign import DeleteCampaign
from BaseRequest.CampaignReport import CampaignReport

from ujson import loads


class CampaignReportHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = CampaignReportForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await CampaignReport.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class DeleteCampaignHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}

        form = DeleteCampaignForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await DeleteCampaign.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class UpdateCampaignHandler(BaseHandler):

    async def post(self):
        param = loads(self.request.body.decode('utf8'))
        form = UpdateCampaignForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        text = await UpdateCampaign.post(self.application.session, form)

        try:
            data = loads(text)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetCampaignInfoHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}

        form = GetCampaignInfoFrom.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetACampaignInfo.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetAllCampaignHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}

        form = BaseForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetAllCampaign.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
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
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
