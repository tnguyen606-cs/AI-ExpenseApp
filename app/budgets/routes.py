from flask import render_template, url_for, flash, redirect, Blueprint
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
        if income > budget:
            new_budget = Budget(month=form.month.data,
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
