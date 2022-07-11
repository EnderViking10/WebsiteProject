from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    backup_code = PasswordField('Backup Code', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
