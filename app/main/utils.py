from flask import request
from app import db
from app.models import Expense, Budget
from datetime import datetime, timedelta


def get_num_expenses(from_date):
    num_item = 0
    table = Expense.query.all()
    for row in table:
        if row.date_spend >= from_date:
            print(row.date_spend)
            num_item = num_item + 1
    return num_item


def get_total_expenses(from_date, to_date):
    sum = Expense.query.with_entities(
        db.func.round(db.func.sum(Expense.amount), 2)).filter(Expense.date_spend >= from_date, Expense.date_spend <= to_date).all()[0]
    return sum


def get_total_income():
    # Case 1: from_month < to_month
    # if from_month < to_month:
    #     sum = Budget.query.with_entities(
    #         db.func.round(db.func.sum(Budget.income), 2)).filter(Budget.id >= from_month, Budget.id <= to_month).all()[0]
    #     print("1", sum[0])
    #     return sum[0]
    # elif from_month > to_month:
    #     sum = Budget.query.with_entities(
    #         db.func.round(db.func.sum(Budget.income), 2)).filter(Budget.id >= from_month, Budget.id <= 12).all()[0]
    #     # sum_2 = Budget.query.with_entities(
    #     #     db.func.round(db.func.sum(Budget.income), 2)).filter(Budget.id >= 1, Budget.id <= to_month).all()[0]
    #     print("2", to_month)
    #     return sum[0]
    # else:
    #     sum = Budget.query.with_entities(
    #         db.func.round(db.func.sum(Budget.income), 2)).filter(Budget.id >= from_month, Budget.id < to_month).all()[0]
    #     print("3", to_month)
    #     return sum[0]
    return Budget.query.with_entities(db.func.round(db.func.sum(Budget.income), 2)).all()[0]


def get_date_str(date_time, format):
    return date_time.strftime(format)


def get_date_datetime(str, format):
    return datetime.strptime(str, format)


def get_date_str_to_num(str):
    return datetime.strptime(str, '%B').month


def pagination(Table, ROWS_PER_PAGE):
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    # This line creates a list of all the expenses sorted by date_spend
    expenses = Table.query.order_by(
        Table.date_spend.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    return expenses


def get_time_period(period, date):
    if period == "Current day":
        return Expense.query.filter(Expense.date_spend == date).order_by(
            Expense.date_spend.desc()).all()
    elif period == "Previous day":
        onedayearly = date - timedelta(days=1)
        return Expense.query.filter(
            Expense.date_spend == onedayearly).order_by(
            Expense.date_spend.desc()).all()
    elif period == "Last 7 days":
        last7days = date - timedelta(days=7)
        return Expense.query.filter(
            Expense.date_spend >= last7days).order_by(
            Expense.date_spend.desc()).all()
    elif period == "Last 14 days":
        last14days = date - timedelta(days=14)
        return Expense.query.filter(
            Expense.date_spend >= last14days).order_by(
            Expense.date_spend.desc()).all()
    elif period == "Last 1 month":
        lastmonth = date - timedelta(days=30)
        return Expense.query.filter(
            Expense.date_spend >= lastmonth).order_by(
            Expense.date_spend.desc()).all()
    else:
        last2months = date - timedelta(days=61)
        return Expense.query.filter(
            Expense.date_spend >= last2months).order_by(
            Expense.date_spend.desc()).all()
