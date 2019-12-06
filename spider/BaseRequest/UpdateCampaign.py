from BaseRequest.BaseApi import BaseApi
from tools.get_time_schedule import get_schedule


class UpdateCampaign(BaseApi):

    @staticmethod
    async def post(session, form):
        params = {
            'title': form.title.data,
            'budget': form.budget.data,
            'promoteTime': get_schedule(form.promoteTime.data),
            'promoteArea': form.promoteArea.data,
            'cositeFlag': form.cositeFlag.data,
            'id': form.id.data,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/campaign/updateCampaign.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=params) as resp:
            text = await resp.text()

        return text
