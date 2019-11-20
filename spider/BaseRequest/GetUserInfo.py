from BaseRequest.BaseApi import BaseApi


class GetUserInfo(BaseApi):

    @staticmethod
    async def get(form, session):
        async with session.get('https://p4p.1688.com/home/ajGetLoginInfo.html?',
                               timeout=5,
                               cookies={'_csrf_token': form.csrf_token.data, 'cookie2': form.cookie2.data}) as resp:
            text = await resp.text()

        return text
