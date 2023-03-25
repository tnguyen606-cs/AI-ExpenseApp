from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Expense


class SearchForm(FlaskForm):
    time_period = SelectField(validators=[DataRequired()], choices=[
                              "All transactions", "Current day", "Previous day", "Last 7 days", "Last 14 days", "Last 1 month", "Last 2 months"])
    submit = SubmitField("Search")
