from pprint import pprint as pp
from time import time, sleep

from requests import get, post


def get_message():
    resp = get('https://p4p.1688.com/home/ajGetLoginInfo.html?', cookies=cookies).json()
    print(resp)


def delete_adgroup_keyoword():
    data = {
        'mergeKeyword': '零食',
        'campaignId': 817580098,
        '_page_csrf_token': cookies['_csrf_token']
    }

    resp = get('https://p4p.1688.com/keyword/deleteKeyword.html', params=data, cookies=cookies)
    print(resp.text)


def get_adgrouid_by_campaign():
    data = {
        'campaignId': 817580098
    }

    resp = get('https://p4p.1688.com/adGroup/listAdGroupSimpleNew.html', cookies=cookies, params=data)
    pp(resp.json())


def get_adgroup_info_by_adgroupid():
    data = {
        'adGroupIds': '391882934,389232465',
        '_page_csrf_token': cookies['_csrf_token']
    }

    resp = get('https://p4p.1688.com/adGroup/listAdGroup.html', params=data, cookies=cookies)
    print(resp.text)


def get_campaign_report():
    data = {
        'startTime': '2019-11-14',
        'endTime': '2019-11-14',
        'campaignIds': '816829371,817580098,816508540',
        '_page_csrf_token': cookies['_csrf_token']
    }

    resp = post('https://p4p.1688.com/report/getCampaignReport.html', data=data, cookies=cookies)
    print(resp.text)


def delete_campaign_by_campaignid():
    data = {
        'campaignIds': 817580136,
        '_page_csrf_token': cookies['_csrf_token']
    }

    resp = get('https://p4p.1688.com/campaign/deleteCampaign.html', params=data, cookies=cookies)
    print(resp.text)


if __name__ == '__main__':
    # 12.9换新的cookies2
    cookies = {'_csrf_token': '1575870554089', 'cookie2': '1a0119a10f74f0ea10b6c1c350fb0ea7'}

    # delete_adgroup_keyoword()
    # get_adgroupid_by_campaign()
    # get_adgroup_info_by_adgroupid()
    # get_campaign_report()
    # delete_campaign_by_campaignid()

    while 1:
        try:
            result = get_message()
            sleep(300)
        except Exception as e:
            print(time())
            break
