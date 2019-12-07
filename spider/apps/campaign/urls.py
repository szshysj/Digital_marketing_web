from tornado.web import url
from apps.campaign.handler import AddCampaignHandler, GetAllCampaignHandler, GetCampaignInfoHandler, \
    UpdateCampaignHandler, DeleteCampaignHandler, CampaignReportHandler

urls_pattern = [
    url('/post/add/campaign/', AddCampaignHandler),
    url('/get/campaign/', GetAllCampaignHandler),
    url('/get/campaign/info/', GetCampaignInfoHandler),
    url('/update/campaign/', UpdateCampaignHandler),
    url('/delete/campaign/', DeleteCampaignHandler),
    url('/get/campaign/report/', CampaignReportHandler)
]
