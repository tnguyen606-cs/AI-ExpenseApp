from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.expenses.forms import ExpenseForm
from app.models import Expense
from app.expenses.utils import send_sms_to

expenses = Blueprint('expenses', __name__)


@expenses.route("/expense/add", methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        new_expense = Expense(title=form.title.data, amount=form.amount.data,
                              date_spend=form.date_spend.data,
                              category=form.category.data,
                              merchant=form.merchant.data,
                              user=current_user, date_posted=today_date)
        db.session.add(new_expense)
        db.session.commit()
        flash('Your new expense has been created!', 'success')
        # message = client.messages.create(
        #     to=send_sms_to(),
        #     from_="+18776647341",
        #     body="We noticed you just added a new expense with an amount of {}!".format(
        #         new_expense.amount)
        # )
        return redirect(url_for('head.home'))
    elif request.method == 'GET':
        form.date_spend.data = today_date
    return render_template('create_expense.html', title='New Expense', form=form, legend='New Expense')


@expenses.route("/expense/<int:expense_id>")
@login_required
def expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense.html', title=expense.title, expense=expense)


@expenses.route("/expense/<int:expense_id>/update", methods=['GET', 'POST'])
@login_required
def expense_update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.date_spend = form.date_spend.data
        expense.category = form.category.data
        expense.merchant = form.merchant.data
        expense.date_posted = datetime.now()
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('expenses.expense', expense_id=expense.id))
    elif request.method == 'GET':
        form.title.data = expense.title
        form.amount.data = expense.amount
        form.date_spend.data = expense.date_spend
        form.category.data = expense.category
        form.merchant.data = expense.merchant
    return render_template('create_expense.html', title='Edit Expense',
                           form=form, legend='Edit Expense')


@expenses.route("/expense/<int:expense_id>/delete", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    # message = client.messages.create(
    #     to=send_sms_to(),
    #     from_="+18776647341",
    #     body="We noticed you just deleted an expense with an amount of {}!".format(
    #         expense.amount)
    # )
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('head.home'))
