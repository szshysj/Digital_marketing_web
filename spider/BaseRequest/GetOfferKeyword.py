from BaseRequest.BaseApi import BaseApi


class GetOfferKeyword(BaseApi):

    @staticmethod
    async def post(session, form):
        params = {
            'campaignId': form.campaignId.data,
            'adGroupIdList': form.adGroupIdList.data,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/keyword/listRecommendKeyword.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=params) as resp:
            text = await resp.text()

        return text
