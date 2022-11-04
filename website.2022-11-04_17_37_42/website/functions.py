from flask import render_template
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import (
    AnonymousUserMixin
)


def render(address, **kwargs):
    return render_template(address,
                           **kwargs)


# Form shown in /login
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Авторизоваться')


def get_profile_type(current_user):
    if isinstance(current_user, AnonymousUserMixin):
        return 0
    return current_user._data["profile_type"]
