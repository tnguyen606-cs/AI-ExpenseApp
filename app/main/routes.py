from flask import render_template, request, Blueprint, flash
from flask_login import login_required
from app import db
from app.models import Expense, Budget, Goal
from app.main.forms import SearchForm
from app.main.utils import get_num_expenses, get_total_expenses, get_date_str, pagination, get_time_period, get_total_income, get_date_str_to_num
from datetime import datetime, timedelta
head = Blueprint('head', __name__)

TODAY = datetime.now()


@head.route("/")
def main():
    return render_template('main.html')


@head.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    # TODO: PAGINATION. Retrieve only five entries per page.
    expenses = pagination(Expense, 5)

    # TODO: BUDGET TRACK
    currentMonth = get_date_str(TODAY, "%B")
    current_budget = Budget.query.filter_by(month=currentMonth).first()

    # TODO: EXPENSES TRACK
    m = get_date_str_to_num(currentMonth)
    input_dt = datetime(2023, m, 1)
    num_expenses = get_num_expenses(input_dt)
    total_expenses = get_total_expenses(input_dt, TODAY)[0]

    # TODO: LEFTOVER CASH FLOW
    if current_budget is not None:
        current_budget.left_cash = round(
            current_budget.budget - total_expenses, 2)
        db.session.commit()
    else:  # This is no month has been created, Create it
        current_budget = []

    # TODO: GOAL TRACK
    current_goal = Goal.query.order_by(Goal.date_posted.asc()).first()
    if current_goal is not None:
        # Format: total_saving = total_income - total_expense in date range
        # saving_from = get_date_str_to_num(
        #     get_date_str(current_goal.date_start, '%B'))
        # saving_to = get_date_str_to_num(
        #     get_date_str(current_goal.date_end, '%B'))
        # last_date =
        # all_expense = get_total_expenses(current_goal.date_start, )
        # all_expenses = get_total_expenses(
        #     current_goal.date_start, current_goal.date_end)
        total_income = get_total_income()[0]
        all_expenses = get_total_expenses(datetime(2023, 1, 1), TODAY)[0]
        current_goal.amount_saving = round(total_income - all_expenses, 2)
        db.session.commit()
    else:
        current_goal = []

    # TODO: SEARCH
    search_form = SearchForm()
    is_pagination = False
    if search_form.validate_on_submit():
        period = search_form.time_period.data
        if period == "All transactions":
            is_pagination = True
        else:
            expenses = get_time_period(period, TODAY)

    return render_template('home.html',
                           expenses=expenses,
                           num_expenses=num_expenses,
                           total_expenses=total_expenses,
                           currentMonth=currentMonth,
                           current_budget=current_budget,
                           left_cash=current_budget.left_cash,
                           current_goal=current_goal,
                           form=search_form,
                           is_pagination=is_pagination)
