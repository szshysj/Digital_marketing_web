from Digital_marketing.models import BaseModel

from peewee import FixedCharField, DateTimeField, CharField


class Account_Info(BaseModel):
    csrf_token = FixedCharField(max_length=13, null=False, verbose_name='账号凭证之一')
    cookie2 = FixedCharField(max_length=32, null=False, verbose_name='账号凭证之二')
    login_id = CharField(max_length=30, null=False, primary_key=True, verbose_name='登录账号')
    member_id = CharField(max_length=30, null=False, verbose_name='官方正版接口 会员id')
    update_time = DateTimeField(null=False, verbose_name='更新时间')
