from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AjaxForm(FlaskForm):
    a = IntegerField('a', validators=[DataRequired()])
    b = IntegerField('b', validators=[DataRequired()])