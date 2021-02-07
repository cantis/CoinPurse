from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo

from web import db

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_bp.route('/signup', methods=['GET'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    return 'Logout'


@auth_bp.route('/profile', methods=['GET'])
def profile():
    return 'Profile'


class LoginForm(FlaskForm):
    """ Login Form """
    email = EmailField(validators=[InputRequired('Please enter your email.')])
    password = PasswordField(validators=[InputRequired('Please enter your password.')])
    remember_me = BooleanField()
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    """ Signup Form """
    first_name = StringField(validators=[InputRequired('Please enter your firstname.')])
    last_name = StringField(validators=[InputRequired('Please enter your last name.')])
    email = EmailField(validators=[InputRequired('Please enter your email.')])
    password = PasswordField(validators=[InputRequired('Please enter a password.'), EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField()
    submit = SubmitField('Sign Up')
