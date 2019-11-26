from tornado.web import url
from apps.keyword.handler import GetOfferKeywordHandler, GetOfferKeywordCpcHandler, AddOfferKeywordHandler, \
    GetAdgroupKeywordListHandler, AddKeywordToMysqlHandler

urls_pattern = [
    url('/get/offer/keyword/', GetOfferKeywordHandler),
    url('/post/offer/keyword/cpc/', GetOfferKeywordCpcHandler),
    url('/post/offer/keyword/', AddOfferKeywordHandler),
    url('/get/adgroup/keyword/', GetAdgroupKeywordListHandler),
    url('/post/mysql/keyword/', AddKeywordToMysqlHandler)
]
