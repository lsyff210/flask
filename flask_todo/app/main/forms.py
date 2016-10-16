from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_babel import gettext as _


class ThingForm(Form):
    thing = StringField(label=_('thing to do'), validators=[DataRequired()])
    submit = SubmitField(label=_('add'))


class EditForm(Form):
    id = IntegerField(label='update1', validators=[DataRequired()])
    thing = StringField(label='update', validators=[DataRequired()])
    submit = SubmitField(label=_('complete'))


class DeleteForm(Form):
    delete_id = IntegerField(label='Delete_id', validators=[DataRequired()])
    submit = SubmitField(label=_('Delete'))

