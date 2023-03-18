from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, ValidationError


class BudgetForm(FlaskForm):
    purpose = SelectField("What's your goal?", choices=["Buy a Car",
                                                        "Buy a Home", "Investment", "Pay Off Debt", "Retirement", "Emergency Fund", "Travel", "College", "Improve Credit Score", "Other"],
                          validators=[DataRequired()])
    title = StringField('Name your goal:', validators=[DataRequired()])
    amount = DecimalField('How much do you want to save?',
                          validators=[DataRequired()])
    date_start = DateField('When do you want to start?',
                           validators=[DataRequired()])
    date_end = DateField('When do you need it by?',
                         validators=[DataRequired()])
    period = SelectField('Save', choices=["Daily", "Weekly", "Bi-Weekly", "Monthly"],
                         validators=[DataRequired()])
    submit = SubmitField('Create Goal')

    def validate_date(self, date_start, date_end):
        valid_date = (date_end.data - date_start.data) > 0
        if not valid_date:
            raise ValidationError(
                'Please select a valid date.')
