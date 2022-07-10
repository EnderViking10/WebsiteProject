from flask_wtf import FlaskForm
from wtforms import SubmitField


class UserPageForm(FlaskForm):
    password_change = SubmitField('Password Change')
