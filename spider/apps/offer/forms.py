from Digital_marketing.forms import CampaignForm

from wtforms import IntegerField
from wtforms.validators import NumberRange, DataRequired


class GetOfferForm(CampaignForm):
    skip = IntegerField('页码', validators=[
        DataRequired(message='请输入页码'),
        NumberRange(min=1, max=99, message='请输入正确的页码范围')
    ])
