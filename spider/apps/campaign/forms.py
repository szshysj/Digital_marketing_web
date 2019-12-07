from Digital_marketing.forms import BaseForm

from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, AnyOf, Regexp


class CampaignReportForm(BaseForm):
    start = StringField('起始日期', validators=[
        DataRequired(message='请输入起始日期'),
        Regexp(regex='.*(\\d{4}-\\d{2}-\\d{2}).*', message='请输入正确的日期格式')])

    end = StringField('起始日期', validators=[
        DataRequired(message='请输入起始日期'),
        Regexp(regex='.*(\\d{4}-\\d{2}-\\d{2}).*', message='请输入正确的日期格式')])


class DeleteCampaignForm(BaseForm):
    campaignIds = StringField('推广计划id列表', validators=[DataRequired(message='请输入推广计划id列表')])


class GetCampaignInfoFrom(BaseForm):
    id = IntegerField('推广计划id', validators=[
        DataRequired(message='请输入推广计划id'),
        NumberRange(min=100000000, max=999999999, message='请输入推广计划id正确的范围')])


class AddCampaignForm(BaseForm):
    title = StringField('推广计划标题', validators=[
        DataRequired(message='请输入标题'),
        Length(min=1, max=60, message='请输入正确的长度')])

    budget = IntegerField('推广计划预算', validators=[
        DataRequired(message='请输入推广计算预算'),
        NumberRange(min=60, max=100, message='请输入正确的预算')])

    promoteArea = StringField('推广计划投放地域', validators=[DataRequired(message='请填写投放地域')])

    cositeFlag = StringField('是否定向推广', validators=[
        DataRequired(message='请填写是否允许定向推广'),
        AnyOf(values=['1', '0'])])

    promoteTime = StringField('推广计划投放时间', validators=[
        DataRequired(message='请填写投放时间'),
        AnyOf(values=['1', '2', '3', '4', '5', '6', '7', '8', '9'])])


class UpdateCampaignForm(GetCampaignInfoFrom, AddCampaignForm):
    pass
