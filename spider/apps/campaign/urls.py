from tornado.web import url
from apps.campaign.handler import AddCampaignHandler, GetAllCampaignHandler

urls_pattern = [
    url('/post/add/campaign/', AddCampaignHandler),
    url('/get/campaign/', GetAllCampaignHandler)
]
