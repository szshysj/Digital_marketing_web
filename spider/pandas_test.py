import pandas as pd
from time import time, perf_counter
from sender import data, cpc, b
from requests import post, get
from pprint import pprint as pp

"""
    {'adGroupId': 390628199, 'adGroupTitle': '', 'auditReason': '', 'auditState': 0, 'b2bOfferId': 0,
     'basePrice': '',
     'bidPrice': '', 'bidPriceMobile': '', 'bidPricePC': '', 'bidPrices': '', 'blackFlag': 0, 'budget': '',
     'campaignId': 0, 'campaignKeywordMode': 0, 'campaignPriceMode': 0, 'campaignState': 0, 'campaignTitle': '',
     'campaignType': 0, 'click': 0, 'containsSmartKeyword': 0, 'containsSmartPrice': 0, 'cositeClick': 0,
     'count': 0,
     'customerId': 0, 'focusFlag': 0, 'gmtCreate': None, 'gmtModified': None, 'groupState': 0, 'id': 0,
     'imgUrl': '',
     'inquiryCount': 0, 'isDefaultPrice': 0, 'keyword': '糖', 'keywordAddErrorReason': '', 'keywordCheckVO': None,
     'keywords': '', 'linkUrl': '', 'locus': 0, 'mlrReasonType': 0, 'model': 0, 'oldPrice': '', 'onlineState': 0,
     'pv': 10000, 'rank': 0, 'rankMobile': 0, 'rankPC': 0, 'recommendReason': '同行词', 'recommendScore': 2147483647,
     'recommendTags': ['同行词', '热搜词'], 'relativity': 8, 'relativityReason': '', 'relativityReasonDetail': None,
     'repeatFlag': 0, 'searchHeat': 3, 'show': 0, 'state': 0, 'suggestFlag': 0, 'suggestFlagMobile': 0,
     'suggestFlagPC': 0, 'suggestPrice': '', 'suggestPriceMobile': '', 'suggestPricePC': '', 'topNAdgroupId': 0,
     'topNCount': 0, 'topNFlag': 0, 'topNKeywordId': 0, 'unityWord': '', 'validFlag': 0}
"""

"""
    {'countBuyer': 3000, 'gmtCreate': 'Thu Nov 21 07:25:16 CST 2019', 'gmtModified': 'Thu Nov 21 07:25:16 CST 2019',
     'id': 0, 'keyword': '糖', 'keywordList': [], 'leftAvgClick7days': 0.59, 'leftAvgPV7days': 1.6400000000000001,
     'rightAvgClick7days': 0, 'rightAvgPV7days': 0, 'searchAvg7days': 4000}
"""

# df_1 = pd.DataFrame(data['data']['recommendKeywordVOList'], columns=['keyword', 'recommendTags'])
# df_2 = pd.DataFrame(cpc['data']['listVOREST'],
#                     columns=['countBuyer', 'leftAvgClick7days', 'leftAvgPV7days', 'searchAvg7days', 'keyword'])
#
# result = pd.merge(df_1, df_2, on='keyword')
# result = result.rename(columns={'countBuyer': '竞争指数', 'leftAvgClick7days': '点击率', 'leftAvgPV7days': '平均出价',
#                                 'searchAvg7days': '展示指数', 'keyword': '关键词', 'recommendTags': '推荐理由'})
#
# result = result[(result['竞争指数'] > 0) & (result['点击率'] > 0) & (result['平均出价'] > 0) & (result['展示指数'] > 0)]


# for result in result.values:
#     tmp_list = []
#     tmp_list.append(result[0])
#     tmp_list.append(result[1])
#     tmp_list.append(result[2])
#     tmp_list.append(round(result[3], 2))
#     tmp_list.append(round(result[4], 2))
#     tmp_list.append(result[5])
#     temp_list.append(tmp_list)

# print(temp_list)
#
data = {
    'keyword_list': b,
    'csrf_token': '1574730102511',
    'cookie2': '10e017de5b8669225b455d6afe59485c'
}
resp = post('http://120.77.183.17:8888/post/mysql/keyword/', json=data)
print(resp.text)
