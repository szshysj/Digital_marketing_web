#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2019/10/11 20:48
# @Author  : 孔祥旭
# @Email   : d90159@163.com / 351469076@qq.com

from os.path import join
from time import strftime, localtime

from redis import StrictRedis
from tornado.web import RequestHandler
from aiofiles import open


class BaseHandler(RequestHandler):

    # 浏览器安全验证
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, '
                        'X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass

    async def write_log(self, *args, filename):
        async with open(join(self.application.settings['log_path'],
                             filename + '-' + strftime("%Y-%m-%d", localtime()) + '.log'), 'a') as f:
            await f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '\n' + str(args) + '\n' * 2)

    def error_handle(self, form):
        re_data = {}
        self.set_status(404)
        for field in form.errors:
            re_data[field] = form.errors[field][0]
        return re_data


class RedisHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redis_conn = StrictRedis(**self.settings['redis'])
