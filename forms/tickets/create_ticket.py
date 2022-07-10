from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateTicketForm(FlaskForm):
    title = StringField('Subject', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    save = SubmitField('Save')
