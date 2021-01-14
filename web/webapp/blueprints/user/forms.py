from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username', validators=[DataRequired()])
    email = StringField('Email', id='email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='password', validators=[DataRequired()])
