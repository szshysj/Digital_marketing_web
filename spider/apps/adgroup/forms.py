from Digital_marketing.forms import CampaignForm

from wtforms import StringField
from wtforms.validators import DataRequired


class AddAdgroupForm(CampaignForm):
    b2bOfferIds = StringField('商品id', validators=[DataRequired(message='请输入商品id')])
