from Digital_marketing.handler import BaseHandler
from BaseRequest.GetCampaignOffer import GetCampaignOffer
from apps.offer.forms import GetCampaignForm

from ujson import loads


class GetCampaignOfferHandler(BaseHandler):

    async def get(self):
        param = loads(self.request.body.decode('utf8'))
        form = GetCampaignForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetCampaignOffer.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(404)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
