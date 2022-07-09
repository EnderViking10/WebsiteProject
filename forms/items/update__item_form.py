from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField


class UpdateItemForm(FlaskForm):
    name = StringField('Item Name')
    description = TextAreaField('Description')
    cost = IntegerField('Cost')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')
