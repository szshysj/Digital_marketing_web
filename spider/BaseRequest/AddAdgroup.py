from BaseRequest.BaseApi import BaseApi


class AddAdgroup(BaseApi):

    @staticmethod
    async def post(session, form):
        params = {
            'campaignId': form.campaignId.data,
            'b2bOfferIds': form.b2bOfferIds.data,
            '_page_csrf_token': form.csrf_token.data,
            'smartOfferFlag': 0,
            'wuageOfferIds': form.b2bOfferIds.data
        }

        async with session.post('https://p4p.1688.com/adGroup/addAdGroup.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=params) as resp:
            text = await resp.text()

        return text
