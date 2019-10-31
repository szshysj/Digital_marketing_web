#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/14 17:27
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com


from apps.authorization.models import User
from functools import wraps

from jwt import decode, ExpiredSignature


def authenticated_async(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        jsession = self.request.headers.get('JSESSION', None)
        if jsession:
            try:
                # 对jwt进行解密, 有效期8小时
                send_data = decode(jsession, self.settings['secret_key'], leeway=self.settings['jwt_expire'],
                                   options={'verify_exp': True})
                user_id = send_data['id']
                try:
                    # 从数据库中获取user并设置给_current_user
                    user = await self.application.objects.get(User, memberId=user_id)
                    self._current_user = user
                    # 此处很关键, 包装的函数是协程对象, 必须要await来接收
                    await method(self, *args, **kwargs)
                except User.DoesNotExist:
                    self.set_status(401)
            except ExpiredSignature:
                self.set_status(401)
        else:
            self.set_status(401)

    return wrapper
