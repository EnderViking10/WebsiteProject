from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField
from wtforms.validators import DataRequired


class AdminPageForm(FlaskForm):
    username = SearchField('Username', validators=[DataRequired()])
    search = SubmitField('Search')