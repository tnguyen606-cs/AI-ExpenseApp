from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=21,
               message="Name length must be between %(min)d and %(max)dcharacters"),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0, "Usernames must have only letters, " "numbers, dots or underscores",
               )])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()])
    password = PasswordField('Password', validators=[
        DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match!")])
    phone = StringField('Phone', validators=[
        DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            user = User.query.filter_by(phone=phone.data).first()
            if not phonenumbers.is_valid_number(p) or user:
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError(
                'Invalid phone number. Please enter a correct phone number.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=21)])
    password = PasswordField('Password', validators=[DataRequired()])
    # This helps Users still stay login for a little while after closing the app
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=5, max=21)])
    email = StringField('Email',
                        validators=[Email()])
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', validators=[
                                     EqualTo('new_password')])
    phone = StringField('Phone')
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError(
                'Invalid phone number. Please enter a correct phone number.')
