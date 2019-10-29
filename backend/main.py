#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 19:45
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from Digital_marketing.urls import urlspatten
from Digital_marketing.settings import settings, database

from uvloop import new_event_loop
from tornado.web import Application
from tornado.platform.asyncio import BaseAsyncIOLoop
from tornado.ioloop import IOLoop
from wtforms_json import init
from peewee_async import Manager


class TornadoUvloop(BaseAsyncIOLoop):

    def initialize(self, **kwargs):
        loop = new_event_loop()
        try:
            super(TornadoUvloop, self).initialize(
                loop, close_loop=True, **kwargs)
        except Exception:
            loop.close()
            raise


if __name__ == '__main__':
    init()  # wtf表单json初始
    app = Application(urlspatten, **settings, debug=True)
    app.listen(8888, address='0.0.0.0')
    objects = Manager(database)
    database.set_allow_sync(False)  # 不允许同步
    app.objects = objects  # 强行设置
    IOLoop.configure(TornadoUvloop)
    IOLoop.current().start()
