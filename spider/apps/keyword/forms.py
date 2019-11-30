from Digital_marketing.forms import AdgroupForm, BaseForm, CampaignForm

from wtforms.validators import DataRequired, Length, Regexp
from wtforms import StringField


class GetAnalyizerResultByWordForm(BaseForm):
    word = StringField('分词后的单个值', validators=[DataRequired(message='请输入分词后的单个值')])
    category = StringField('关键词类目', validators=[
        DataRequired(message='请输入关键词类目'),
        Length(min=1, max=10, message='请输入类目正确的长度')
    ])


class GetAdgroupKeywordListForm(CampaignForm):
    adGroupId = StringField('推广单元id', validators=[
        DataRequired(message='请输入推广单元id'),
        Length(min=9, max=9, message='请输入正确的推广单元id长度'),
        Regexp(regex='\\d{9}', message='请输入正确的推广单元id格式')
    ])


class AddOfferKeywordForm(AdgroupForm):
    keywords = StringField('关键词字符串', validators=[DataRequired(message='请输入关键词')])
    bidPrices = StringField('关键词价格', validators=[DataRequired(message='请输入关键词价格')])


class GetOfferKeywordCpcForm(BaseForm):
    keywords = StringField('关键词字符串', validators=[DataRequired(message='请输入关键词')])


class GetOfferKeywordForm(AdgroupForm):
    pass
