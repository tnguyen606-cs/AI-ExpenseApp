from io import BytesIO
import base64
from app.models import Budget
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')


def get_column_values(path_string, column_name):
    df = pd.read_csv(path_string)
    column_values = df[column_name].tolist()
    return column_values


def create_hover_text(values):
    return [f"${value:,.2f}" for value in values]


def generate_categories(months):
    months_amount = {
        'Earned': [],
        'Spent': [],
    }
    # Generate month/income/budget lists of values from database
    month_values = [row[0] for row in Budget.query.with_entities(
        Budget.month).order_by(Budget.id.asc()).all()]
    income_values = [row[0] for row in Budget.query.with_entities(
        Budget.income).order_by(Budget.id.asc()).all()]
    left_values = [row[0] for row in Budget.query.with_entities(
        Budget.left_cash).order_by(Budget.id.asc()).all()]
    index = 0
    for key in months:
        if index < len(month_values) and key in month_values[index]:
            months_amount['Earned'].append(income_values[index])
            months_amount['Spent'].append(
                income_values[index] - left_values[index])
            index += 1
        else:
            months_amount['Earned'].append(0)
            months_amount['Spent'].append(0)

    return months_amount


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

    # Add some text for labels, removing spines and custom x-axis, y-axis tick labels, etc.
    max_y = max(max(dict['Earned']), max(dict['Spent']))
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(x_indexes)
    ax.set_xticklabels(x_data)
    ax.set_ylim(0, max_y + 200)
    ax.tick_params(left=True)
    # add a legend
    ax.legend(frameon=False, fontsize=15)

    # convert the plot to an image and encode it as base64
    buffer = BytesIO()  # Save it to a temporary buffer.
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(
        buffer.getvalue()).decode('utf-8').replace('\n', '')

    return image_base64
