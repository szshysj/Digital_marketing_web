from tornado.web import url
from apps.user.handler import GetUserInfoHander, GetUserBalanceHandler

urls_pattern = [
    url('/post/user/info/', GetUserInfoHander),
    url('/get/user/banlance/', GetUserBalanceHandler)
]
