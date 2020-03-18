import datetime
from requests import get, post
from ujson import dumps
from pprint import pprint as pp
from scrapy.selector import Selector


def 实时商品榜单():
    resp = get(base_url + '/portal/getShopHotOffer.json', cookies=cookies).json()
    pp(resp)


def 近30天支付金额排名():
    date = datetime.date.today() - datetime.timedelta(days=1)
    param = {
        'dateType': 'day',
        'dateRange': f'{date}|{date}'
    }
    resp = get(base_url + '/portal/shopSummaryIndex.json', params=param, cookies=cookies).json()
    pp(resp)


def 核心看板():
    resp = get(base_url + '/dataAnomaly.json', cookies=cookies).json()
    pp(resp)


def 商品转化率当天():
    """只能获取前一天数据, 在对比前前一天的数据"""

    param = {
        'order': 'desc',
        'orderBy': 'uv',
        'device': '0',
        'dateRange': '2019-12-04|2019-12-04',
        'dateType': 'day',
        'pageSize': '10',
        'page': '1'
    }
    resp = get(base_url + '/item/itemTop.json', params=param, cookies=cookies).json()
    pp(resp)


def 商品转化率一周():
    param = {
        'order': 'desc',
        'orderBy': 'uv',
        'device': '0',
        'dateRange': '2019-11-25|2019-12-01',
        'dateType': 'week',
        'pageSize': '30',
        'page': '1'
    }
    resp = get(base_url + '/item/itemTop.json', params=param, cookies=cookies).json()
    for _ in resp['data']['data']:
        pp(_)
        break


def 交易看板():
    resp = get(base_url + '/portal/live/overview.json', cookies=cookies).json()
    pp(resp)


def 实时概况():
    resp = get(base_url + '/portal/live/trend.json', cookies=cookies).json()
    pp(resp)


def 当天订单():
    data = {
        'skipBucket': 'true',
        'isBuyer': 'false',
        'startDate': '2019-12-04',
        'startHour': '0',
        'startMinute': '0',
        'endDate': '2019-12-04',
        'endHour': '23',
        'endMinute': '59',
        'tradeStatus': 'waitsellersend'
    }
    resp = get('https://trade.1688.com/order/seller_order_list.htm', params=data, cookies=cookies)
    resp = Selector(text=resp.text)
    # 选择每个li标签
    xpath_list = resp.xpath('//div[@id="bd"]/ul/li')
    for result in xpath_list:
        # 订单号
        # order_id = result.xpath('input[@class="tradeId"]').xpath('@value').get()
        # 订单生成时间
        date = result.xpath('div[@class="title order-title"]/'
                            'div[@class="top fd-clr"]/'
                            'div[@class="left"]/'
                            'div[@class="col-group"]/'
                            'span[@class="date"]/text()').get()
        # 下单类型
        date = result.xpath('div[@class="title order-title"]/'
                            'div[@class="top fd-clr"]/'
                            'div[@class="left"]/'
                            'div[@data-spm="order-biz-type"]/a').xpath('@title').get()
        # 旺旺昵称
        name = result.xpath('div[@class="title order-title"]/'
                            'div[@class="top fd-clr"]/'
                            'div[@class="left"]/'
                            'div[3]/'
                            'span[2]/text()').get()
        # 会员等级
        vip_level = result.xpath('div[@class="title order-title"]/'
                                 'div[@class="top fd-clr"]/'
                                 'div[@class="left"]/'
                                 'div[@class="col-group"]/'
                                 'a/img').xpath('@src').re_first('.*/(.*?).png')
        # 商品链接
        offer_link = result.xpath('.//a[@class="productName"]').xpath('@href').get()
        # 商品标题
        offer_title = result.xpath('.//a[@class="productName"]/text()').getall()
        print(offer_link, offer_title)
        # //div[@id="bd"]/ul/li/div[@class="title order-title"]/div[@class="top fd-clr"]/div[@class="left"]/div[@class="col-group"]/a/img/@src


if __name__ == '__main__':
    # cookies = {'_csrf_token	': '1575443246384', 'cookie2': '175203fa7876f0e9213abb3cfaa83e47'}
    cookies = {'cookie2': '175203fa7876f0e9213abb3cfaa83e47'}
    base_url = 'https://sycm.1688.com/ms'

    # 实时商品榜单()  # 实时, 首页-右上角
    # 交易看板()  # 实时, 首页-上中, 可计算店内转化率
    # 核心看板()  # 实时, 支付金额较前日下跌47.92% 客单价较前日下跌47.92% 新增13个零访问商品  成功退款金额较上周下跌97.41%   店铺行业排名较上周下跌22名
    # 实时概况()  # 实时, 首页-左上, 对比今天和昨天的支付金额, 支付金额是累计

    # 近30天支付金额排名()  # 生意参谋首页-右上角
    # 商品转化率当天()
    # 商品转化率一周() # 可计算单品转化率
    当天订单()
