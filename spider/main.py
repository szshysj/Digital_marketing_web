#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/31 10:36
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.redis import RedisPool
from Digital_marketing.urls import urlspatten
from Digital_marketing.settings import settings, database
from asyncio import get_event_loop, set_event_loop_policy

from uvloop import EventLoopPolicy
from tornado.web import Application
from peewee_async import Manager
from wtforms_json import init


def make_app(loop):
    apps = Application(urlspatten, **settings, debug=True)

    func = RedisPool(loop=loop)

    # redis异步库
    apps.redis = func.get_conn()

    # 异步请求库
    apps.session = func.get_aiohttp()

    # mysql异步ORM库
    objects = Manager(database)
    database.set_allow_sync(False)
    apps.objects = objects

    return apps


if __name__ == '__main__':
    # wtf_tornado表单json初始
    init()

    # uvloop替换asyncio循环
    set_event_loop_policy(EventLoopPolicy())

    # 获取当前事件循环
    loop = get_event_loop()

    # 封装tornado及一系列异步操作库
    app = make_app(loop)
    app.listen(8888, '0.0.0.0')

    # 事件循环启动, 永不停止
    loop.run_forever()
