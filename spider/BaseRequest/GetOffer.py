from BaseRequest.BaseApi import BaseApi


class GetOffer(BaseApi):

    @staticmethod
    async def get(session, form):
        params = {
            'campaignId': form.campaignId.data,
            'skip': form.skip.data,
            'limit': 10,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.get('https://p4p.1688.com/offer/listPromoteOffersMixed.html',
                               timeout=5,
                               cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                               params=params) as resp:
            text = await resp.text()

        return text
