from datetime import datetime


def convert_monthTextToInt(mm):
    return datetime.strptime(mm, '%B').month


def percent_saving(income, budget):
    percent_saving = (income - budget) / income * 100
    return percent_saving > 20
