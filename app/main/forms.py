from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validator=[DataRequired()])
    password = PasswordField('Password', validators=DataRequired())
    remember_me_boolean = BooleanField('Remember Me')
    submit = SubmitField('Sign in')
