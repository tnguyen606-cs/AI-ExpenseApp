from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.budgets.forms import BudgetForm
from app.models import Budget

budgets = Blueprint('budgets', __name__)


@budgets.route("/budgets/add", methods=['GET', 'POST'])
@login_required
def new_budget():
    form = BudgetForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        income = form.income.data
        budget = form.budget.data
        mm = form.month.data
        if income > budget:
            new_budget = Budget(id=datetime.strptime(mm, '%B').month,
                                month=mm,
                                income=form.income.data,
                                budget=budget,
                                user=current_user, date_posted=today_date)
            db.session.add(new_budget)
            db.session.commit()
            flash('Your New Budget has been created!', 'success')
            return redirect(url_for('head.home'))
        else:
            flash(
                'Please enter the income higher than your budget', 'danger')
    return render_template('create_budget.html', title='New Budget', form=form, legend='New Budget')


@budgets.route("/budgets")
@login_required
def budget():
    # This line creates a list of all the budgets sorted by month
    all_budgets = Budget.query.order_by(Budget.id).all()
    # This line loops through all the budgets
    for i in range(len(all_budgets)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_budgets[i].id = len(all_budgets) - i
    db.session.commit()
    return render_template('budgets.html', title="Budgets", budgets=all_budgets)


@budgets.route("/budget/<int:budget_id>/update", methods=['GET', 'POST'])
@login_required
def budget_update(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    form = BudgetForm()
    if form.validate_on_submit():
        if form.income.data > form.budget.data:
            if budget.month != form.month.data or budget.income != form.income.data or budget.left_cash != form.left_cash.data or budget.budget != form.budget.data:
                budget.month = form.month.data
                budget.income = form.income.data
                budget.budget = form.budget.data
                budget.left_cash = form.left_cash.data
                budget.date_posted = datetime.now()
                db.session.commit()
                flash('Your budget has been updated!', 'success')
                return redirect(url_for('budgets.budget'))
            else:
                flash('There is no update!', 'danger')
        else:
            flash(
                'Please enter the income higher than your budget', 'danger')
    elif request.method == 'GET':
        form.month.data = budget.month
        form.income.data = budget.income
        form.budget.data = budget.budget
        form.left_cash.data = budget.left_cash
    return render_template('update_budget.html', title='Update Budget',
                           form=form, legend='Update Budget', budget_id=budget_id)


@budgets.route("/budget/<int:budget_id>/delete", methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    # message = client.messages.create(
    #     to=send_sms_to(),
    #     from_="+18776647341",
    #     body="We noticed you just deleted an expense with an amount of {}!".format(
    #         expense.amount)
    # )
    db.session.delete(budget)
    db.session.commit()
    flash('Your budget has been deleted!', 'success')
    return redirect(url_for('head.home'))