from flask import render_template, Blueprint
from flask_login import login_required
from app import db
from app.models import Expense, Budget, Goal
from app.main.forms import SearchForm
from app.main.utils import get_date_str, pagination, get_time_period, get_total_income, get_date_datetime, expenses_csv, budgets_csv, goals_csv
from datetime import datetime
import pandas as pd

head = Blueprint('head', __name__)

TODAY = datetime.now()  # datetime.datetime
CURR_MONTH = get_date_str(TODAY, "%B")


@head.route("/")
def main():
    return render_template('main.html')


@head.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    # TODO: PAGINATION. Retrieve only five entries per page.
    expenses = pagination(Expense, 5)

    # Create/Update CVS Files
    expenses_csv()
    budgets_csv()
    goals_csv()

    # READ CVS FILE
    df_expenses = pd.read_csv("./instance/files/user_expenses.csv")

    # TODO: QUERY EXPENSES TRACK of the current month
    int_m = get_date_datetime(CURR_MONTH, '%B').month
    # Convert date_column to datetime type
    df_expenses['Date Spend'] = pd.to_datetime(df_expenses['Date Spend'])
    num_expenses = df_expenses.loc[df_expenses['Date Spend']
                                   >= datetime(2023, int_m, 1), 'Amount'].count()
    total_expenses = float(df_expenses.loc[df_expenses['Date Spend']
                                           >= datetime(2023, int_m, 1), 'Amount'].sum())
    total_expenses = round(total_expenses, 2)

    # TODO: QUERY BUDGET AND CALCULATE LEFTOVER CASH FLOW
    left_cash = 0
    # get the value of the 'budget' column where the 'month' column is 'currentMonth'
    current_budget = Budget.query.filter_by(month=CURR_MONTH).first()
    if current_budget is not None:
        left_cash = round(current_budget.budget - total_expenses, 2)
        current_budget.left_cash = left_cash
        db.session.commit()
    else:  # No month has been created, display it as NONE
        current_budget = []

    # TODO: QUERY GOAL, get the most created goal
    current_goal = Goal.query.order_by(Goal.date_posted.asc()).first()
    if current_goal is not None:
        from_month = get_date_datetime(get_date_str(
            current_goal.date_start, "%Y"), '%Y').month
        to_month = get_date_datetime(get_date_str(
            current_goal.date_end, "%Y"), '%Y').month
        from_year = get_date_datetime(get_date_str(
            current_goal.date_start, "%Y"), '%Y').year
        to_year = get_date_datetime(get_date_str(
            current_goal.date_end, "%Y"), '%Y').year
        # SUM all budgets based on months
        total_budget = get_total_income(
            from_month, to_month, from_year, to_year)
        # SUM all expenses from date_start to date_end
        total_expenses_from_to = df_expenses.loc[(df_expenses['Date Spend'] >= current_goal.date_start)
                                                 & (df_expenses['Date Spend'] <= current_goal.date_end), 'Amount'].sum()
        current_goal.amount_saving = round(
            total_budget - total_expenses_from_to, 2)
        db.session.commit()
    else:
        current_goal = []

    # TODO: SEARCH
    search_form = SearchForm()
    is_pagination = True
    if search_form.validate_on_submit():
        period = search_form.time_period.data
        if period == "All transactions":
            is_pagination = True
        else:
            is_pagination = False
            expenses = get_time_period(period, TODAY)

    return render_template('home.html',
                           expenses=expenses,
                           num_expenses=num_expenses,
                           total_expenses=total_expenses,
                           currentMonth=CURR_MONTH,
                           current_budget=current_budget,
                           left_cash=left_cash,
                           current_goal=current_goal,
                           form=search_form,
                           is_pagination=is_pagination)
