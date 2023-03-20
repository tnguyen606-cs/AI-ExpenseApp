from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.budgets.forms import BudgetForm
from app.models import Budget
from app.budgets.utils import calculateSavingAmount, duration

budgets = Blueprint('budgets', __name__)


@budgets.route("/budgets/add", methods=['GET', 'POST'])
@login_required
def new_goal():
    form = BudgetForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        date_start = form.date_start.data
        date_end = form.date_end.data
        dur = duration(date_start, date_end)
        if dur > 30:
            amount = form.amount.data
            period = form.period.data
            amount_saving = calculateSavingAmount(dur, amount, period)
            new_goal = Budget(title=form.title.data,
                              purpose=form.purpose.data,
                              amount=amount,
                              date_start=date_start,
                              date_end=date_end,
                              period=period,
                              amount_saving=amount_saving,
                              user=current_user, date_posted=today_date)
            db.session.add(new_goal)
            db.session.commit()
            flash('Your New Goal has been created!', 'success')
            return redirect(url_for('head.home'))
        else:
            flash(
                'Please select the number of saving dates greater than 30 days!', 'danger')
    return render_template('create_budget.html', title='New Goal', form=form, legend='New Goal')
