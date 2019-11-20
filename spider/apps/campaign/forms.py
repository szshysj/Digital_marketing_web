from Digital_marketing.forms import BaseForm

from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, AnyOf


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
