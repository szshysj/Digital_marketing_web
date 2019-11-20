from Digital_marketing.handler import BaseHandler
from apps.adgroup.forms import AddAdgroupForm
from BaseRequest.AddAdgroup import AddAdgroup

from ujson import loads


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
