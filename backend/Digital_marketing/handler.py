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

    @staticmethod
    def get_schedule(type_num):
        """
        全天 7*24小时
        热门时间段  上午10点到12点   下午3点到6点    晚上9点到11点
        闲时 晚上9点到早上6点

        :param type_num: 时段类型
        :return: 具体的值
        """

        schedule_dict = {
            # 7*24 全天
            1: '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111111111111111111111111111',
            # 7*24 热门
            2: '000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000011000111000110',
            # 7*24 闲时
            3: '111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111111111000000000000000111',
            # 工作日 全天
            4: '000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111'
               '111111111111111111111111111111111111111111111000000000000000000000000',
            # 工作日 热门
            5: '000000000000000000000000000000000011000111000110000000000011000111000110000000000011000111000110000'
               '000000011000111000110000000000011000111000110000000000000000000000000',
            # 工作日 闲时
            6: '000000000000000000000000111111000000000000000111111111000000000000000111111111000000000000000111111'
               '111000000000000000111111111000000000000000111000000000000000000000000',
            # 休息日 全天
            7: '111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111111111111111111111',
            # 休息日 热门
            8: '000000000011000111000110000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000000000000011000111000110',
            # 休息日 闲时
            9: '111111000000000000000111000000000000000000000000000000000000000000000000000000000000000000000000000'
               '000000000000000000000000000000000000000000000111111000000000000000111'
        }

        return schedule_dict[type_num]