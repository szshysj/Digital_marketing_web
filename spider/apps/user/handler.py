from Digital_marketing.handler import BaseHandler
from Digital_marketing.forms import BaseForm
from BaseRequest.GetUserInfo import GetUserInfo
from BaseRequest.GetUserBalance import GetUserBalance
from apps.user.forms import GetUserInfoForm
from apps.user.models import Account_Info
from datetime import datetime

from ujson import loads


class GetUserBalanceHandler(BaseHandler):

    async def get(self):
        params = self.request.arguments
        params = {param[0]: param[1][0].decode('utf8') for param in params.items()}
        form = BaseForm.from_json(params)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        resp = await GetUserBalance.get(self.application.session, form)

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        await self.finish(data)


class GetUserInfoHander(BaseHandler):

    async def post(self):

        param = loads(self.request.body.decode('utf8'))
        form = GetUserInfoForm.from_json(param)

        if not form.validate():
            return await self.finish(self.error_handle(form))

        # ====================================我是分割线======================================================
        resp = await GetUserInfo.get(form, self.application.session)

        # ====================================我是分割线======================================================

        try:
            data = loads(resp)
        except ValueError:
            self.set_status(401)
            return await self.finish({'msg': '状态失效, 需要重新登录'})

        # ====================================我是分割线======================================================

        try:
            user = await self.application.objects.get(Account_Info, member_id=data['data']['user']['memberID'])
            user.csrf_token = data['data']['csrfToken']
            user.cookie2 = form.cookie2.data
            user.update_time = datetime.now()
            await self.application.objects.update(user)
        except Account_Info.DoesNotExist:
            await self.application.objects.create(Account_Info,
                                                  csrf_token=data['data']['csrfToken'],
                                                  cookie2=form.cookie2.data,
                                                  login_id=data['data']['user']['loginID'],
                                                  member_id=data['data']['user']['memberID'],
                                                  update_time=datetime.now())

        await self.finish({'csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data})
