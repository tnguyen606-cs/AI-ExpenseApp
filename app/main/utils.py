from app import db
from datetime import datetime


def get_num_rows(table_name):
    count = db.session.query(table_name).count()
    return count


def get_expense_amount(table_name):
    sum = table_name.query.with_entities(
        db.func.round(db.func.sum(table_name.amount), 2)).all()[0]
    return sum


def get_total_expenses_inrange(list):
    sum = 0
    for item in list:
        sum = sum + item.amount
    return sum


def get_month():
    return datetime.now().strftime("%B")
