from flask import render_template, request, Blueprint
from flask_login import login_required
from app import db
from app.models import Expense, Budget, Goal
from app.main.utils import get_num_rows, get_expense_amount, get_month
head = Blueprint('head', __name__)


@head.route("/")
def main():
    return render_template('main.html')


@head.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    # This line creates a list of all the expenses sorted by date_spend
    expenses = Expense.query.order_by(
        Expense.date_spend.desc()).paginate(page=page, per_page=5)

    # TODO: EXPENSES TRACK
    num_expenses = get_num_rows(Expense)
    total_expenses = get_expense_amount(Expense)

    # TODO: BUDGET TRACK
    currentMonth = get_month()
    current_budget = Budget.query.filter_by(month=currentMonth).first()

    # TODO: LEFTOVER CASH FLOW
    left_cash = 0
    saving_amount = 0
    if current_budget is not None:
        current_budget.left_cash = current_budget.budget - total_expenses[0]
        db.session.commit()
        left_cash = current_budget.left_cash
        saving_amount = current_budget.income - total_expenses[0]
    else:  # This is no month has been created, Create it
        current_budget = []

    # TODO: GOAL TRACK
    currennt_goal = Goal.query.order_by(Goal.date_posted.desc()).first()
    if currennt_goal is not None:
        currennt_goal.amount_saving = saving_amount
        db.session.commit()
    else:
        currennt_goal = []

    return render_template('home.html',
                           expenses=expenses,
                           num_expenses=num_expenses,
                           total_expenses=total_expenses,
                           currentMonth=currentMonth,
                           current_budget=current_budget,
                           left_cash=left_cash,
                           currennt_goal=currennt_goal)
