from Digital_marketing.forms import CampaignForm, BaseForm

from wtforms import StringField
from wtforms.validators import DataRequired


class DeleteAdgroupForm(BaseForm):
    adGroupIds = StringField('请输入推广单元id', validators=[DataRequired(message='请输入推广单元id列表')])


class GetCampaignAdgroupForm(CampaignForm):
    pass


class AddAdgroupForm(CampaignForm):
    b2bOfferIds = StringField('商品id', validators=[DataRequired(message='请输入商品id')])
