from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired


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
