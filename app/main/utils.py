import os
import pandas as pd
from flask import request, current_app
from app import db
from app.models import Expense, Budget, Goal
from datetime import datetime, timedelta


def get_total_income(from_month, to_month, from_year, to_year):
    df_budgets = pd.read_csv("./instance/files/user_budgets.csv")
    delta_years = to_year - from_year
    if delta_years == 0 and from_month < to_month:
        return df_budgets.loc[(df_budgets['ID'] >= from_month)
                              & (df_budgets['ID'] <= to_month), 'Budget'].sum()
    else:
        budget = df_budgets.loc[(df_budgets['ID'] >= from_month)
                                & (df_budgets['ID'] <= 12), 'Budget'].sum()
        return budget + df_budgets.loc[(df_budgets['ID'] >= 1)
                                       & (df_budgets['ID'] <= to_month), 'Budget'].sum()


def pagination(data, ROWS_PER_PAGE):
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    # This line creates a list of all the expenses sorted by date_spend
    expenses = data.query.order_by(
        data.date_spend.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    return expenses


def get_date_str(date_time, format):
    return date_time.strftime(format)


def get_date_datetime(str, format):
    return datetime.strptime(str, format)


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


#  Queries all Expenses from the database, converts them to a pandas DataFrame, and writes the DataFrame to a CSV file.
def expenses_csv():
    # Create csv file in python_ flask
    path = os.path.join(
        current_app.root_path, '../instance/files')
    if not os.path.exists(path):
        os.makedirs(path)
    cvs_path = os.path.join(path, 'user_expenses.csv')
    expenses = Expense.query.all()
    if expenses is not None:
        df = pd.DataFrame([(e.id, e.title, e.amount, e.date_spend.strftime('%m/%d/%Y'), e.category, e.merchant, e.user_id, e.date_posted)
                           for e in expenses], columns=['ID', 'Title', 'Amount', 'Date Spend', 'Category', 'Merchant', 'User_ID', 'Date Posted'])
        df.to_csv(cvs_path, index=False)

#  Queries all Budget from the database, converts them to a pandas DataFrame, and writes the DataFrame to a CSV file.


def budgets_csv():
    # Create csv file in python_ flask
    path = os.path.join(
        current_app.root_path, '../instance/files')
    if not os.path.exists(path):
        os.makedirs(path)
    cvs_path = os.path.join(path, 'user_budgets.csv')
    budgets = Budget.query.all()
    if budgets is not None:
        df = pd.DataFrame([(e.id, e.month, e.income, e.budget, e.left_cash, e.user_id, e.date_posted)
                           for e in budgets], columns=['ID', 'Month', 'Income', 'Budget', 'Leftover Cash', 'User_ID', 'Date Posted'])
        df.to_csv(cvs_path, index=False)

#  Queries all Goal from the database, converts them to a pandas DataFrame, and writes the DataFrame to a CSV file.


def goals_csv():
    path = os.path.join(
        current_app.root_path, '../instance/files')
    if not os.path.exists(path):
        os.makedirs(path)
    cvs_path = os.path.join(path, 'user_goals.csv')
    goals = Goal.query.all()
    if goals is not None:
        df = pd.DataFrame([(e.id, e.title, e.purpose, e.amount, e.date_start, e.date_end, e.period, e.amount_saving, e.user_id, e.date_posted)
                           for e in goals], columns=['ID', 'Title', 'Purpose', 'Amount', 'Date Start', 'Date End', 'Period', 'Amount Saving', 'User_ID', 'Date Posted'])
        # Create csv file in python_ flask
        df.to_csv(cvs_path, index=False)
