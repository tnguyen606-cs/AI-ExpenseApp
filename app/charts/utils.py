import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from app.models import Budget
import base64
from io import BytesIO


def get_column_values(path_string, column_name):
    df = pd.read_csv(path_string)
    column_values = df[column_name].tolist()
    return column_values


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

def grouped_bars_chart(dict, x_data):

    # create a figure and axis object
    fig, ax = plt.subplots(layout='constrained')

    # Array for horizontal bar's position
    x_indexes = np.arange(len(x_data))  # the label locations
    width = 0.5  # the width of the bars
    multiplier = 0

    # plot the grouped bars
    colors = ['#54f0c9', '#f5788e']
    i = 0
    for l in dict:
        offset = width * multiplier
        rects = ax.bar(x_indexes + offset,
                       dict[l], width, color=colors[i], label=l)
        ax.bar_label(rects, padding=5)
        multiplier += 0.75
        i += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    max_y = max(max(dict['Earned']), max(dict['Spent']))
    min_y = min(min(dict['Earned']), min(dict['Spent']))
    ax.set_xticks(x_indexes + 0.25, x_data)
    ax.set_yticks([])
    ax.set_ylabel('Amount ($)')
    ax.set_ylim(min_y, max_y + 250)
    ax.legend()

    # convert the plot to an image and encode it as base64
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(
        buffer.getvalue()).decode('utf-8').replace('\n', '')
    
    return image_base64
