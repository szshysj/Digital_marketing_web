# from scapy.all import *
#
# stars = lambda n: "*" * n
#
# def GET_print(packet):
#     return "\n".join((
#         stars(10) + "GET PACKET" + stars(10),
#         "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n")),
#         stars(30)))
#
# sniff(
#     iface='Intel(R) Wireless-AC 9560 160MHz',
#     prn=GET_print,
#     lfilter=lambda p: "GET" in str(p),
#     filter="tcp")

from pprint import pprint as pp
from time import perf_counter, time
from jieba import cut, lcut_for_search
from requests import get
from redis import Redis

import time
import redis

number_list = ['300033', '300032', '300031', '300030']
signal = ['1', '-1', '1', '-1']

rc = redis.StrictRedis(host='120.77.183.17', port='6379', db=3, password='********')
for i in range(len(number_list)):
    value_new = str(number_list[i]) + ' ' + str(signal[i])
    rc.publish("liao", value_new)  # 发布消息到liao
