from Digital_marketing.models import BaseModel

from peewee import FixedCharField, DateTimeField, CharField, SmallIntegerField, FloatField, PrimaryKeyField


class Offer_Keyword_7days(BaseModel):
    keyword = CharField(max_length=10, null=False, verbose_name='关键词')
    recommendTags = CharField(max_length=30, null=False, verbose_name='推荐理由')
    countBuyer = SmallIntegerField(null=False, verbose_name='竞争指数')
    leftAvgClick7days = FloatField(null=False, verbose_name='点击率')
    leftAvgPV7days = FloatField(null=False, verbose_name='平均出价')
    searchAvg7days = SmallIntegerField(null=False, verbose_name='展示指数')
    update_time = DateTimeField(null=False, verbose_name='更新时间')
    # is_delete          tinyint(1) 0 未删除  1 逻辑删除


class Offer_Keyword(BaseModel):
    id = PrimaryKeyField(verbose_name='主键id')
    keyword = CharField(max_length=10, null=False, unique=True, verbose_name='关键词')
    recommendTags = CharField(max_length=30, null=False, verbose_name='推荐理由')
    countBuyer = SmallIntegerField(null=False, verbose_name='竞争指数')
    leftAvgClick7days = FloatField(null=False, verbose_name='点击率')
    leftAvgPV7days = FloatField(null=False, verbose_name='平均出价')
    searchAvg7days = SmallIntegerField(null=False, verbose_name='展示指数')
    keyword_update_time = DateTimeField(null=False, verbose_name='官方关键词更新时间')
    # update_time        TimestampField
    # is_delete          tinyint(1) 0 未删除  1 逻辑删除


class Account_Info(BaseModel):
    csrf_token = FixedCharField(max_length=13, null=False, verbose_name='账号凭证之一')
    cookie2 = FixedCharField(max_length=32, null=False, verbose_name='账号凭证之二')
    login_id = CharField(max_length=30, null=False, primary_key=True, verbose_name='登录账号')
    member_id = CharField(max_length=30, null=False, verbose_name='官方正版接口 会员id')
    update_time = DateTimeField(null=False, verbose_name='更新时间')
