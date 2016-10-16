# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo
from flask_babel import gettext as _


class RegistrationForm(Form):
    username = StringField(
        label=_('name'),
        validators=[DataRequired(),
                    Regexp(r'^[a-zA-Z][a-zA-Z0-9_.]*?$', flags=0, message=_('name must begin with a-z or A-Z'))])
    password = PasswordField(label=_('password'),
                             validators=[DataRequired(), EqualTo('password2', message=_('password must be same'))])
    password2 = PasswordField(label=_('again password'), validators=[DataRequired()])
    email = StringField(label=_('email'), validators=[DataRequired(), Email()])
    submit = SubmitField(label=_('register'))


class LoginForm(Form):
    username = StringField(label=_('name'), validators=[DataRequired()])
    password = PasswordField(label=_('password'), validators=[DataRequired()])
    submit = SubmitField(label=_('login'))