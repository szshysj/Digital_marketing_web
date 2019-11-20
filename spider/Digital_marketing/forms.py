from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class BaseForm(Form):
    csrf_token = StringField('账号认证之一', validators=[
        DataRequired(message='请输入csrf_token'),
        Length(min=13, max=13, message='csrf_token长度有误')
    ])

    cookie2 = StringField('账号认证之二', validators=[
        DataRequired(message='请输入cookie2'),
        Length(min=32, max=32, message='cookie2长度有误')
    ])


class CampaignForm(BaseForm):
    campaignId = StringField('推广计划id', validators=[
        DataRequired(message='请输入推广计划id'),
        Length(min=9, max=9, message='推广计划id长度错误'),
        Regexp(regex='\\d{9}', message='推广计划id格式错误')
    ])


class AdgroupForm(CampaignForm):
    adGroupIdList = StringField('推广单元id', validators=[
        DataRequired(message='请输入推广单元id'),
        Length(min=9, max=9, message='推广单元id长度错误'),
        Regexp(regex='\\d{9}', message='推广计划id格式错误')
    ])
