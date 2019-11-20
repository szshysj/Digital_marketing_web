from BaseRequest.BaseApi import BaseApi


class AddOfferKeyword(BaseApi):

    @staticmethod
    async def post(session, form):
        data = {
            'campaignId': form.campaignId.data,
            'adGroupIdList': form.adGroupIdList.data,
            'keywords': form.keywords.data,
            'bidPrices': form.bidPrices.data,
            'keywordMode': 2,
            'priceMode': 3,
            'userAddCount': 0,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.post('https://p4p.1688.com/keyword/addKeywordWithBidPriceMixed.html',
                                timeout=5,
                                cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                                data=data) as resp:
            text = await resp.text()

        return text
