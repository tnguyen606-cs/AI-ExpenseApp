from flask import render_template, request, Blueprint
from flask_login import login_required
from datetime import datetime
from app import db
from app.models import Expense, Budget, Goal
from app.main.utils import get_num_rows, get_total_amount, get_total_expenses_inrange
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
    # TODO: Count number of expenses
    num_expenses = get_num_rows(Expense)
    # TODO: Sum total of expenses
    total_expenses = get_total_amount(Expense)
    # TODO: Display the month of budget
    currentMonth = datetime.now().strftime("%B")
    # TODO: Display the budget of the month
    current_budget = Budget.query.filter_by(month=currentMonth).first_or_404(
        description='There is no budget has been created with {}'.format(currentMonth))
    # TODO: Display the Leftover Cash
    left_cash = current_budget.budget - total_expenses[0]
    current_budget.left_cash = left_cash
    # TODO: Display the Goal's Name
    goal = Goal.query.order_by(
        Goal.date_posted.desc()).first()
    noGoal = True if goal is None else False
    # TODO: Display the Goal's total saving_amount
    today_date = datetime.now()

    # range = Expense.query.filter(goal.date_start <= Budget.date_spend,
    #                              goal.date_end >= Budget.date_spend).all()
    # expenses_within = get_total_expenses_inrange(range)
    total_saving = left_cash + goal.amount_saving
    goal.amount_saving = total_saving
    # Update DATABASES
    db.session.commit()
    print(total_saving)
    return render_template('home.html',
                           expenses=expenses,
                           num_expenses=num_expenses,
                           total_expenses=total_expenses,
                           currentMonth=currentMonth,
                           current_budget=current_budget,
                           left_cash=left_cash,
                           goal=goal,
                           noGoal=noGoal)
