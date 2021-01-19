from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Regexp, Length, EqualTo, DataRequired, ValidationError
from flaskmusic.models import User


class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=64),
                                            Regexp(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 0,
                                                   'Email must have "@" and "."')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=64),
                                            Regexp(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 0,
                                                   'Email must have "@" and "."')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=64),
                                            Regexp(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 0,
                                                   'Email must have "@" and "."')])
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.username:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=64),
                                            Regexp(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 0,
                                                   'Email must have "@" and "."')])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ArtistForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    song = StringField('Song', validators=[DataRequired()])
    album = StringField('Album', validators=[DataRequired()])
    submit = SubmitField('Submit')