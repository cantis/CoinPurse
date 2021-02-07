from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo

from web import db
from web.models import User

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        if user is not None:
            if check_password_hash(user.password, password):
                return redirect(url_for('entry_bp.index'))

    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/signup', methods=['GET'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='sha256')
        )

        # check if the user exists
        user = User.query.filter_by(email=new_user.email).first()
        if user:
            # user exists, go back to signup
            return redirect(url_for('auth_bp.signup'))

        # User doesn't exist add them, then to login form
        db.session.add(new_user)
        db.session.commit
        return redirect(url_for('auth_bp.login'))

    else:
        # Invalid form, back to signup
        return redirect(url_for('auth_bp.signup'))


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
