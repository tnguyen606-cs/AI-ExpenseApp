def calculateSavingPeriod(duration, amount, period):
    # saving amount per day
    money = round(amount / duration, 2)
    # Find the amount saving based on the days
    if period == "Daily":
        return money
    elif period == "Weekly":
        days = 7
        return money * days
    elif period == "Bi-Weekly":
        days = 14
        return money * days
    else:
        days = 30
        return money * days


def duration(date_start, date_end):
    return (date_end - date_start).days
