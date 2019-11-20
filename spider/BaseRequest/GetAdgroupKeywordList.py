from BaseRequest.BaseApi import BaseApi


class GetAdgroupKeywordList(BaseApi):

    @staticmethod
    async def get(session, form):
        params = {
            'queryType': 1,
            'campaignId': form.campaignId.data,
            'adGroupId': form.adGroupId.data,
            'limit': 1000,
            'skip': 0,
            'blackFlag': 0,
            '_page_csrf_token': form.csrf_token.data
        }

        async with session.get('https://p4p.1688.com/keyword/listKeyword.html',
                               timeout=5,
                               cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data},
                               params=params) as resp:
            text = await resp.text()

        return text
