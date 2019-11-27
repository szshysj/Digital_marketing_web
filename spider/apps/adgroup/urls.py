from tornado.web import url
from apps.adgroup.handler import AddAdgroupHandler, GetCampaignAdgroupHandler, GetCampaignAdgroupInfoHandler

urls_pattern = [
    url('/post/adgroup/', AddAdgroupHandler),
    url('/get/campaign/adgroup/', GetCampaignAdgroupHandler),
    url('/get/campaign/adgroup/info/', GetCampaignAdgroupInfoHandler)
]
