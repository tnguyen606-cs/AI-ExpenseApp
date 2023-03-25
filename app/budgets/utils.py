from app import db
from datetime import datetime
from app.models import Expense


def convert_monthTextToInt(mm):
    return datetime.strptime(mm, '%B').month


def percent_saving(income, budget):
    percent_saving = (income - budget) / income * 100
    return percent_saving > 20


def get_total_expenses(from_date, to_date):
    sum = Expense.query.with_entities(
        db.func.round(db.func.sum(Expense.amount), 2)).filter(Expense.date_spend >= from_date, Expense.date_spend <= to_date).all()[0]
    return sum


def get_date_str_to_num(str):
    return datetime.strptime(str, '%B').month
