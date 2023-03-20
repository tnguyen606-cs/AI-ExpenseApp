from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Budget


class BudgetForm(FlaskForm):
    month = SelectField("Month", choices=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                        validators=[DataRequired()])
    income = IntegerField('Income budget', validators=[DataRequired()])
    budget = IntegerField('Monthly budget', validators=[DataRequired()])
    submit = SubmitField('Create Budget')

    def validate_month(self, month):
        if Budget.query.filter_by(month=month.data).first():
            raise ValidationError(
                "Please enter different month or go back to update the existing monthly budget!")
