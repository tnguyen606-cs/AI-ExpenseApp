from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime


class GoalForm(FlaskForm):
    purpose = SelectField("What's your goal?", choices=["Buy a Car",
                                                        "Buy a Home", "Investment", "Pay Off Debt", "Retirement", "Emergency Fund", "Travel", "College", "Improve Credit Score", "Other"],
                          validators=[DataRequired()])
    title = StringField('Name your goal', validators=[DataRequired()])
    amount = DecimalField('How much do you want to save?', places=2,
                          validators=[DataRequired()])
    date_start = DateField('When do you want to start?',
                           validators=[DataRequired()])
    date_end = DateField('When do you need it by?',
                         validators=[DataRequired()])
    period = SelectField('Saving', choices=["Daily", "Weekly", "Bi-Weekly", "Monthly"],
                         validators=[DataRequired()])
    submit = SubmitField('Create Goal')

    def validate_date_start(self, date_start):
        # The date_start has to be after the current date to start
        if date_start.data.strftime("%Y-%m-%d") < datetime.now().strftime("%Y-%m-%d"):
            raise ValidationError(
                "Please enter the saving date begins from today or afterwards!")


class GoalUpdateForm(FlaskForm):
    title = StringField('Name of your goal:', validators=[DataRequired()])
    amount = DecimalField('Amount you wanted to save:', places=2,
                          validators=[DataRequired()])
    date_start = DateField('Saving starts on:',
                           validators=[DataRequired()])
    date_end = DateField('Saving ends on:',
                         validators=[DataRequired()])
    period = SelectField('Track your saving every:', choices=["Daily", "Weekly", "Bi-Weekly", "Monthly"],
                         validators=[DataRequired()])
    submit = SubmitField('Save Goal')
