from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.budget.forms import BudgetForm
from app.models import Budget
from app.budget.utils import calculateSavingAmount

budgets = Blueprint('budgets', __name__)


@budgets.route("/budget/add", methods=['GET', 'POST'])
@login_required
def new_goal():
    form = BudgetForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        new_goal = Budget(title=form.title.data,
                          purpose=form.purpose.data,
                          amount=form.amount.data,
                          date_start=form.date_start.data,
                          date_end=form.date_end.data,
                          period=form.period.data,
                          user=current_user, date_posted=today_date)
        db.session.add(new_goal)
        db.session.commit()
        flash('Your New Goal has been created!', 'success')
        return redirect(url_for('head.home'))
    elif request.method == 'GET':
        form.date_start.data = today_date
        form.date_end.data = today_date
    return render_template('create_budget.html', title='New Goal', form=form, legend='New Goal', period=form.period.data, amount=form.amount.data)