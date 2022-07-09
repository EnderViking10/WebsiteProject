from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms import validators


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email = EmailField('Email', validators=[validators.Length(min=6, max=35)])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
