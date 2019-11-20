from tornado.web import url
from apps.adgroup.handler import AddAdgroupHandler

urls_pattern = [
    url('/post/adgroup/', AddAdgroupHandler)
]
