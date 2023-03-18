def calculateSavingAmount(date_start, date_end, amount, period):
    duration = (date_end - date_start).days
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
