# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_babel import Babel, gettext as _

class LoginForm(Form):
    username = StringField(label=_(u'用户名'), validators=[DataRequired()])
    password = PasswordField(label=_(u'密码'), validators=[DataRequired()])
    submit = SubmitField(label=_(u'登录'))


class RegistrationForm(Form):
    email = StringField(label=_(u'邮箱'), validators=[DataRequired(message=_(u'邮箱不能为空')), Email(message=_(u'请输入正确的邮箱地址')), Length(1, 64)])
    username = StringField(label=_(u'用户名'), validators=[DataRequired(), Length(1, 64),
                                                        Regexp('^[a-zA-Z][a-zA-Z0-9_.]*$', 0,
                                                               _(u'用户名必须由字母数、字数、下划线或 . 组成'))])
    password = PasswordField(label=_(u'密码'), validators=[DataRequired(), EqualTo('password2', message=_(u'两次输入的密码必须一致'))])
    password2 = PasswordField(label=_(u'密码'), validators=[DataRequired()])
    submit = SubmitField(label=_(u'马上注册'))

