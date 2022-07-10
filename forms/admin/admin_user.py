from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class AdminUserForm(FlaskForm):
    user_level = SelectField('Username', choices=[(0, 'Member'), (1, 'Moderator'), (2, 'Administrator')])
    restriction_level = SelectField('Restriction Level', choices=[(0, 'Unrestricted'), (1, 'Restricted')])
    submit = SubmitField('Submit')
