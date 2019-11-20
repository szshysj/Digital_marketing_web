from Digital_marketing.forms import AdgroupForm, BaseForm

from wtforms.validators import DataRequired
from wtforms import StringField


class AddOfferKeywordForm(AdgroupForm):
    keywords = StringField('关键词字符串', validators=[DataRequired(message='请输入关键词')])
    bidPrices = StringField('关键词价格', validators=[DataRequired(message='请输入关键词价格')])


class GetOfferKeywordCpcForm(BaseForm):
    keywords = StringField('关键词字符串', validators=[DataRequired(message='请输入关键词')])


class GetOfferKeywordForm(AdgroupForm):
    pass
