from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.goals.forms import GoalForm, GoalUpdateForm
from app.models import Goal
from app.goals.utils import duration, calSavingPeriod

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
        if dur >= 30:
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
            return redirect(url_for('goals.list_goal'))
        else:
            flash(
                'Please select the number of saving dates greater than 30 days!', 'danger')
    return render_template('create_goal.html', title='New Goal', form=form, legend='New Goal')


@goals.route("/goals")
@login_required
def list_goal():
    # This line creates a list of all the goals
    all_goals = Goal.query.all()
    print(all_goals)
    return render_template('goals.html', title="Goals", goals=all_goals)


@goals.route("/goal/<int:goal_id>/update", methods=['GET', 'POST'])
@login_required
def goal_update(goal_id):
    goal = Goal.query.filter(Goal.id == goal_id).first()
    print(goal.id)
    form = GoalUpdateForm()
    if form.validate_on_submit():
        dur = duration(form.date_start.data, form.date_end.data)
        if dur >= 30:
            goal.title = form.title.data
            goal.amount = form.amount.data
            goal.date_start = form.date_start.data
            goal.date_end = form.date_end.data
            goal.period = form.period.data
            db.session.commit()
            flash('Your goal has been saved!', 'success')
            return redirect(url_for('goals.list_goal'))
        else:
            flash(
                'Please select the number of saving dates greater than 30 days!', 'danger')
    elif request.method == 'GET':
        form.title.data = goal.title
        form.amount.data = goal.amount
        form.date_start.data = goal.date_start
        form.date_end.data = goal.date_end
        form.period.data = goal.period
    durr = duration(goal.date_start, goal.date_end)
    saving_regular = calSavingPeriod(durr, goal.amount, goal.period)
    return render_template('goal_update.html', title=goal.purpose,
                           form=form, legend=goal.purpose, saving_regular=saving_regular, period=goal.period)


@goals.route("/goals/<int:goal_id>/delete", methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.filter(Goal.id == goal_id).first()
    print(goal)
    # message = client.messages.create(
    #     to=send_sms_to(),
    #     from_="+18776647341",
    #     body="We noticed you just deleted an expense with an amount of {}!".format(
    #         expense.amount)
    # )
    db.session.delete(goal)
    db.session.commit()
    flash('Your goal has been deleted!', 'success')
    return redirect(url_for('goals.list_goal'))
