from apps.offer.handler import GetOfferHandler

from tornado.web import url

urls_pattern = [
    url('/get/offer/', GetOfferHandler)
]
