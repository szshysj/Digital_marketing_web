from BaseRequest.BaseApi import BaseApi
from tools.get_time_schedule import get_schedule


class AddCampaign(BaseApi):

    @staticmethod
    async def post(form, session):
        data = {
            'title': form.title.data,
            'budget': form.budget.data,
            'promoteArea': form.promoteArea.data,
            'promoteAreaText': '全部区域',
            'cositeFlag': form.cositeFlag.data,
            'promoteTime': get_schedule(form.promoteTime.data),
            'promoteTimeText': '全部时段',
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/campaign/addCampaign.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=data) as resp:
            text = await resp.text()

        return text
