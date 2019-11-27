from BaseRequest.BaseApi import BaseApi


class GetCampaignAdgroupInfo(BaseApi):

    @staticmethod
    async def get(session, form):
        params = {
            'adGroupIds': form['adGroupIds'],
            '_page_csrf_token': form['csrf_token']
        }

        async with session.get('https://p4p.1688.com/adGroup/listAdGroup.html',
                               timeout=5,
                               cookies={'_csrf_token': form['csrf_token'], 'cookie2': form['cookie2']},
                               params=params) as resp:
            text = await resp.text()

        return text
