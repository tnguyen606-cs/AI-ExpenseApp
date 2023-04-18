from io import BytesIO
import base64
import random
from app.models import Budget
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')


def round_number(num):
    return round(float(num), 2)


def get_column_values(path_string, column_name):
    df = pd.read_csv(path_string)
    column_values = df[column_name].tolist()
    return column_values


def create_hover_text(values):
    return [f"${value:,.2f}" for value in values]


def calculate_amount_spent(months):
    monthly_amount = {
        'Earned': [],
        'Spent': [],
    }
    # Generate month/income/budget lists of values from database
    month_values = [row[0] for row in Budget.query.with_entities(
        Budget.month).order_by(Budget.id.asc()).all()]
    income_values = [row[0] for row in Budget.query.with_entities(
        Budget.income).order_by(Budget.id.asc()).all()]
    leftover_values = [row[0] for row in Budget.query.with_entities(
        Budget.left_cash).order_by(Budget.id.asc()).all()]
    index = 0
    for key in months:
        if index < len(month_values) and key in month_values[index]:
            monthly_amount['Earned'].append(income_values[index])
            monthly_amount['Spent'].append(
                income_values[index] - leftover_values[index])
            index += 1
        else:
            monthly_amount['Earned'].append(0)
            monthly_amount['Spent'].append(0)

    return monthly_amount


def plot_bars_chart(dict, x_data):

    # create a figure and axis object
    fig, ax = plt.subplots(layout='constrained')

    #  set the position of the bars on the x-axis: Array for horizontal bar's position
    x_indexes = np.arange(len(x_data))  # the label locations
    # set the width of each bar
    bar_width = 0.45

    # create the bars for each group
    ax.bar(x_indexes - bar_width/2 + 0.1,
           dict['Earned'], width=bar_width, color='#54f0c9', label='Earned')
    ax.bar(x_indexes + bar_width/2 - 0.05,
           dict['Spent'], width=bar_width, color='#f5788e', label='Spent')

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Add some text for labels, removing spines and custom x-axis, y-axis tick labels, etc.
    max_y = max(max(dict['Earned']), max(dict['Spent']))
    ax.set_xticks(x_indexes, fontsize=10, horizontalalignment='center')
    ax.set_xticklabels(x_data)
    ax.set_ylim(0, max_y + 200)
    ax.tick_params(left=True)
    # add a legend
    ax.legend(loc='best', fontsize=12)

    # convert the plot to an image and encode it as base64
    buffer = BytesIO()  # Save it to a temporary buffer.
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(
        buffer.getvalue()).decode('utf-8').replace('\n', '')

    return image_base64


def plot_horizontal_chart(money_earned, money_limit, money_spent):
    # Calculate the difference between earned and spent
    diff = money_earned - money_spent

    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(3.3, 0.3))

    # Create the stacked bar chart
    ax.barh([0], diff, color='#f5788e', label='Money Spent')
    ax.barh([0], money_earned, left=diff,
            color='#e5e5e6', label='Money Earned')

    # Add the threshold line
    ax.axvline(money_limit, color='#656565')

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Set the x-axis, y-axis label and limits to nothing
    ax.set_xticks([])
    ax.set_yticks([])

    # Add a legend
    ax.legend().remove()

    buffer = BytesIO()  # Save it to a temporary buffer.
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(
        buffer.getvalue()).decode('utf-8').replace('\n', '')

    return image_base64


def get_expenses(before_date):
    df_expenses = pd.read_csv("./instance/files/user_expenses.csv")
    df_expenses['Date Spend'] = pd.to_datetime(df_expenses['Date Spend'])
    filteredDF = df_expenses.loc[(df_expenses['Date Spend'] >= before_date)]
    return filteredDF


def get_month_expense(fist_date_of_month):
    # Calculate the total expenses group by categories
    filteredDF = get_expenses(fist_date_of_month)
    groupedDF = filteredDF.groupby(
        'Category', as_index=False, sort=False).sum()
    sortedDF = groupedDF.sort_values('Amount', ascending=False)
    amount_dict = sortedDF.set_index('Category')['Amount'].to_dict()
    return amount_dict


def generate_random_cl():
    color = "#ff"+''.join([random.choice('0123456789ABCDEF')
                          for _ in range(4)])
    return color


def my_autopct(pct):
    return ('%1.1f%%' % pct) if pct > 5 else ''


def plot_pie_chart(mydict, myColors):
    # Calculate the total expenses:
    total_expenses = sum(mydict.values())

    # Calculate the percentage of each category of expenses:
    percentages = [mydict[val]/total_expenses*100 for val in mydict]

    fig, ax = plt.subplots(figsize=(3.3, 3.5))
    # Plot the pie graph:
    _, _, autopcts = ax.pie(percentages, autopct=my_autopct, colors=myColors, radius=1.35, startangle=90,
                            wedgeprops=dict(width=0.65, edgecolor='w'), pctdistance=0.75)
    plt.setp(autopcts, **{'color': '#1c1919',
             'weight': 'bold', 'fontsize': 12.5})
    # Save it to a temporary buffer.
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(
        buffer.getvalue()).decode('utf-8').replace('\n', '')

    return plot_data


def get_spending(since_date):
    filteredDF = get_expenses(since_date)
    return filteredDF.groupby('Date Spend', as_index=False, sort=True).sum()


def update_data_list(data_list, insert_val, append_val):
    data_list.insert(0, insert_val)
    data_list.append(append_val)
    return data_list


def plot_area_chart(date_data, spending_data, last_spending_data):
    # create data frames for the current and last month
    current_month_data = pd.DataFrame(
        {'Current Month Spending': spending_data},
        index=np.arange(len(spending_data)))
    last_month_data = pd.DataFrame(
        {'Last Month Spent': last_spending_data},
        index=np.arange(len(last_spending_data)))

    # merge the two data frames and fill missing values with 0
    data = current_month_data.merge(
        last_month_data, how='outer', left_index=True, right_index=True).fillna(0)

    # create a plot of the data
    fig, ax = plt.subplots(layout='constrained')
    ax.fill_between(date_data, data['Current Month Spending'],
                    color='#54f0c9', alpha=0.6, linewidth=2)
    ax.plot(date_data, data['Current Month Spending'],
            color='#118c6b', linewidth=2)
    ax.plot(date_data, data['Last Month Spent'],
            color='#118c6b', alpha=0.4, linewidth=2)
    min_val = min(min(data['Current Month Spending']),
                  min(data['Last Month Spent']))
    max_val = max(max(data['Current Month Spending']),
                  max(data['Last Month Spent']))
    ax.set_ylim(min_val - 10, max_val + 20)
    plt.xticks(date_data[::2], fontsize=10, horizontalalignment='center')

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # save the plot to a PNG image in memory
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # encode the image in base64 format and return it as a string
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return plot_data
