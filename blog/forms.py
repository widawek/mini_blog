from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is_published?')
