from tornado.web import url
from apps.adgroup.handler import AddAdgroupHandler, GetCampaignAdgroupHandler, GetCampaignAdgroupInfoHandler, \
    DeleteAdgroupHandler

urls_pattern = [
    url('/post/adgroup/', AddAdgroupHandler),
    url('/get/campaign/adgroup/', GetCampaignAdgroupHandler),
    url('/get/campaign/adgroup/info/', GetCampaignAdgroupInfoHandler),
    url('/delete/adgroup/', DeleteAdgroupHandler)
]
