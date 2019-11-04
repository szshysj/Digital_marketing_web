#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/31 10:49
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

import aioredis
import aiohttp


async def _init_with_loop(loop):
    """
    redis 连接池
    aiohttp 连接池
    :param loop: 循环
    :return: redis pool
    """

    __pool = await aioredis.create_redis_pool(
        'redis://localhost', minsize=5, maxsize=10, encoding='utf8', loop=loop)

    __session = aiohttp.ClientSession()

    return __pool, __session


class RedisPool:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            _loop = kwargs.get("loop", None)
            assert _loop, "use get_event_loop()"
            cls._redis, cls._session = _loop.run_until_complete(_init_with_loop(_loop))
            cls._instance = super(RedisPool, cls).__new__(cls)
        return cls._instance

    def get_conn(self) -> aioredis.Redis:
        return self._redis

    def get_aiohttp(self):
        return self._session
