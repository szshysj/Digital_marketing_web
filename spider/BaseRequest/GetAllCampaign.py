from BaseRequest.BaseApi import BaseApi


class GetAllCampaign(BaseApi):

    @staticmethod
    async def get(session, form):
        params = {
            'queryType': 1,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.get('https://p4p.1688.com/campaign/listCampaignNew.html',
                               timeout=5,
                               cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                               params=params) as resp:
            text = await resp.text()

        return text
