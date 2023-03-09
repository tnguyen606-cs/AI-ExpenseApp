from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class ExpenseForm(FlaskForm):
    title = StringField('Purpose:', validators=[DataRequired()])
    amount = DecimalField('Amount (Maximum 10,000 Dollards):', validators=[
                          DataRequired(), NumberRange(min=0.5, max=10000)])
    date_spend = DateField('Date of Spend:', validators=[DataRequired()])
    category = SelectField('Category:', choices=["Food & Dining",
                                                 "Groceries", "Gas & Fuel", "Bills & Utilities", "Loan", "Shopping", "Transfer", "Other Spending"],
                           validators=[DataRequired()])
    merchant = StringField('Merchant:', validators=[DataRequired()])
    submit = SubmitField('Save Expense')
