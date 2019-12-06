from BaseRequest.BaseApi import BaseApi
from tools.get_time_schedule import get_schedule


class DeleteAdgroup(BaseApi):

    @staticmethod
    async def post(session, form):
        data = {
            'adGroupIds': form.adGroupIds.data,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/adGroup/deleteAdGroup.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=data) as resp:
            text = await resp.text()

        return text
