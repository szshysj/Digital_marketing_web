from tornado.web import url
from apps.offer.handler import GetCampaignOfferHandler

urls_pattern = [
    url('/get/campaign/offer/', GetCampaignOfferHandler)
]
