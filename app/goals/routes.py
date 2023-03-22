from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.goals.forms import GoalForm
from app.models import Goal
from app.goals.utils import duration

goals = Blueprint('goals', __name__)


@goals.route("/goals/add", methods=['GET', 'POST'])
@login_required
def new_goal():
    form = GoalForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        date_start = form.date_start.data
        date_end = form.date_end.data
        dur = duration(date_start, date_end)
        if dur > 30:
            amount = form.amount.data
            period = form.period.data
            new_goal = Goal(title=form.title.data,
                            purpose=form.purpose.data,
                            amount=amount,
                            date_start=date_start,
                            date_end=date_end,
                            period=period,
                            user=current_user, date_posted=today_date)
            db.session.add(new_goal)
            db.session.commit()
            flash('Your New Goal has been created!', 'success')
            return redirect(url_for('head.home'))
        else:
            flash(
                'Please select the number of saving dates greater than 30 days!', 'danger')
    return render_template('create_goal.html', title='New Goal', form=form, legend='New Goal')
