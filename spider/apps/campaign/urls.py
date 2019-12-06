from tornado.web import url
from apps.campaign.handler import AddCampaignHandler, GetAllCampaignHandler, GetCampaignInfoHandler, \
    UpdateCampaignHandler

urls_pattern = [
    url('/post/add/campaign/', AddCampaignHandler),
    url('/get/campaign/', GetAllCampaignHandler),
    url('/get/campaign/info/', GetCampaignInfoHandler),
    url('/update/campaign/', UpdateCampaignHandler)
]
