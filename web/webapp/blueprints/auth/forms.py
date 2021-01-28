from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', id='email', validators=[DataRequired()])
    password = PasswordField('Password', id='password', validators=[DataRequired()])
