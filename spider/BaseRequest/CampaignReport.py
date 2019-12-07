from BaseRequest.BaseApi import BaseApi


class CampaignReport(BaseApi):

    @staticmethod
    async def post(session, form):
        params = {
            'start': form.start.data,
            'end': form.end.data,
            'limit': '1000',
            'skip': '0',
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/datamall/cpc/campaign/feature.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=params) as resp:
            text = await resp.text()

        return text
