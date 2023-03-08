from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=5, max=21)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=5, max=21)])
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


class ExpenseForm(FlaskForm):
    title = StringField('Purpose:', validators=[DataRequired()])
    amount = DecimalField('Amount (Dollards):', validators=[DataRequired(), NumberRange(min=0.5, max=10000)])
    date_spend = DateField('Date of Spend:', validators=[DataRequired()])
    category = SelectField('Category:', choices=["Food & Dining",
                                                 "Groceries", "Gas & Fuel", "Bills & Utilities", "Loan", "Shopping", "Transfer", "Other Spending"],
                           validators=[DataRequired()])
    merchant = StringField('Merchant:', validators=[DataRequired()])
    submit = SubmitField('Save Expense')
