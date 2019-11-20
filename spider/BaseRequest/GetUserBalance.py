from BaseRequest.BaseApi import BaseApi


class GetUserBalance(BaseApi):

    @staticmethod
    async def get(session, form):
        async with session.get('https://p4p.1688.com/account/findAccountDetail.html',
                               timeout=5,
                               cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data}) as resp:
            text = await resp.text()

        return text
