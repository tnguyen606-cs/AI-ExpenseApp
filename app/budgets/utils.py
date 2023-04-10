from app import db
from datetime import datetime
from app.models import Expense


def percent_saving(income, budget):
    percent_saving = (income - budget) / income * 100
    return percent_saving > 20


def get_date_str_to_num(str):
    return datetime.strptime(str, '%B').month


def get_total_expenses(m):
    from_date = datetime(2023, m, 1)
    to_date = datetime(2023, m, 28) if m == 2 else datetime(2023, m, 30)
    sum = Expense.query.with_entities(
        db.func.round(db.func.sum(Expense.amount), 2)).filter(Expense.date_spend >= from_date, Expense.date_spend <= to_date).all()[0]
    print(sum)
    return sum
