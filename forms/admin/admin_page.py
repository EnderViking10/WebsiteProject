from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired


class AdminPageForm(FlaskForm):
    username = SearchField('Username', validators=[DataRequired()])
    search = SubmitField('Search')
