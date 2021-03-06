from Digital_marketing.handler import BaseHandler
from apps.offer.forms import GetOfferForm
from BaseRequest.GetOffer import GetOffer

from ujson import loads


class GetOfferHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}

        form = GetOfferForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetOffer.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)
