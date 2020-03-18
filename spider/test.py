# coding:utf-8
from requests import get, post
from pprint import pprint as pp
from ujson import dumps, loads


# from sender import temp_list


def get_user_info():
    resp = post('http://120.77.183.17/post/user/info/', json=data)
    print(loads(resp.text))


def add_campaign(data_):
    url = 'http://120.77.183.17/post/add/campaign/'
    data_ = {
        'title': '88889999',
        'budget': 60,
        'promoteArea': '2361,2118,1816',
        'cositeFlag': '1',
        'promoteTime': '1',
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2']
    }

    resp = post(url, json=data_).json()
    print(resp)


def get_all_campaign(data_):
    url = 'http://120.77.183.17:8888/get/campaign/?csrf_token=1575507035022&cookie2=175203fa7876f0e9213abb3cfaa83e47'

    resp = get(url).json()
    pp(resp)


def get_campaign_adgroup(data_):
    url = 'http://120.77.183.17:8888/get/campaign/adgroup/'
    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '817274318'
    }

    resp = get(url, params=data_).json()
    pp(resp)


def get_campaign_adgroup_info(data_):
    url = 'http://120.77.183.17:8888/get/campaign/adgroup/info/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'adGroupIds': '394022308,394042749',
    }

    resp = get(url, params=data_).json()
    pp(resp)


def add_adgroup(data_):
    url = 'http://120.77.183.17/post/adgroup/'
    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '817564644',
        'b2bOfferIds': '608083531896,600883154556'
    }

    resp = post(url, json=data_)
    print(resp.text)


def get_user_balance(data_):
    url = 'http://120.77.183.17/get/user/banlance/'
    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2']
    }

    resp = get(url, json=data_).json()
    pp(resp)


def get_offer_keyword(data_):
    url = 'http://120.77.183.17:8888/get/offer/keyword/'
    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '817257331',
        'adGroupIdList': '394294818'
    }

    resp = get(url, params=data_)
    print(resp.text)


def get_offer_keyword_cpc(data_):
    url = 'http://120.77.183.17:8888/post/offer/keyword/cpc/'
    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'keywords': '话梅'
    }

    resp = post(url, json=data_).json()
    print(resp)


def add_offer_keyword(data_):
    url = 'http://120.77.183.17/post/offer/keyword/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '818095209',
        'adGroupIdList': '392011683',
        'keywords': '糖果@@@食品 休闲',
        'bidPrices': '2.0_2.0,2.0_2.0'
    }

    resp = post(url, json=data_).json()
    pp(resp)


def get_adgroup_keyword(data_):
    url = 'http://120.77.183.17/get/adgroup/keyword/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '818095209',
        'adGroupId': '392011683',
    }

    resp = get(url, json=data_).json()
    pp(resp)


def add_keyword_to_mysql():
    url = 'http://120.77.183.17:8888/post/mysql/keyword/'

    data_ = {
        'keyword_list': temp_list
    }

    resp = post(url, json=data_)
    print(resp.text)


def get_offer(data_):
    url = 'http://120.77.183.17:8888/get/offer/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignId': '817250839',
        'skip': '2',
    }

    resp = get(url, params=data_).json()
    pp(resp)


def get_analyizer_result(data_):
    url = 'http://120.77.183.17:8888/get/analyizer/result/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'word': '蜜饯',
        'category': '杨梅干'
    }

    resp = get(url, params=data_).json()
    pp(resp)


def get_campaign_info(data_):
    url = 'http://120.77.183.17:8888/get/campaign/info/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'id': '817274318'
    }

    resp = get(url, params=data_).json()
    pp(resp)


def update_campaign(data_):
    url = 'http://120.77.183.17:8888/update/campaign/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'id': '817274318',
        'title': 'ok啦啦啦',
        'budget': '60',
        'promoteTime': '1',
        'promoteArea': '0',
        'cositeFlag': '1'
    }

    resp = post(url, json=data_).json()
    pp(resp)


def delete_campaign(data_):
    url = 'http://120.77.183.17:8888/delete/campaign/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'campaignIds': '817294971'
    }

    resp = get(url, params=data_).json()
    pp(resp)


def delete_adgroup(data_):
    url = 'http://120.77.183.17:8888/delete/adgroup/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'adGroupIds': '395675179,393916079'
    }

    resp = post(url, json=data_).json()
    pp(resp)


def get_campaign_report(data_):
    url = 'http://120.77.183.17:8888/get/campaign/report/'

    data_ = {
        'csrf_token': data_['csrf_token'],
        'cookie2': data_['cookie2'],
        'start': '2019-11-22',
        'end': '2019-12-06'
    }

    resp = post(url, json=data_).json()
    pp(resp)


if __name__ == '__main__':
    data = {
        'csrf_token': '1575507035022',
        'cookie2': '175203fa7876f0e9213abb3cfaa83e47'
    }
    # add_campaign(data)
    # add_keyword_to_mysql()
    # add_adgroup(data)
    # add_offer_keyword(data)

    # get_user_info()
    # get_all_campaign(data)
    # get_campaign_info(data)
    # get_campaign_adgroup(data)
    # get_campaign_adgroup_info(data)
    # get_user_balance(data)
    # get_offer_keyword(data)
    # get_offer_keyword_cpc(data)
    # get_adgroup_keyword(data)
    # get_offer(data)
    # get_analyizer_result(data)
    get_campaign_report(data)

    # update_campaign(data)

    # delete_campaign(data)
    # delete_adgroup(data)
