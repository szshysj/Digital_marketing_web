from Digital_marketing.forms import CampaignForm

from wtforms.validators import DataRequired, NumberRange
from wtforms import IntegerField


class GetCampaignForm(CampaignForm):
    skip = IntegerField('商品页码数', validators=[
        DataRequired(message='请输入商品页码数'),
        NumberRange(min=1, max=99, message='请输入正确的页码数')
    ])
