#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 10:35
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from ujson import loads


async def get_token(code, session, settings):
    url = 'https://gw.open.1688.com/openapi/http/1/system.oauth2/getToken/' + settings["app_key"]

    params = {
        'grant_type': 'authorization_code',
        'need_refresh_token': 'true',
        'client_id': settings["app_key"],
        'client_secret': settings["app_secret"],
        'redirect_uri': settings["app_callback_url"] + '/get/authorization/',
        'code': code
    }

    async with session.post(url, params=params, timeout=5) as resp:
        status_code = resp.status
        text = await resp.text()

    return status_code, loads(text)
