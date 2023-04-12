from app.charts.utils import round_number, calculate_amount_spent, plot_bars_chart, plot_horizontal_chart, plot_pie_chart, generate_expenses, generate_random_cl
from app import db
from flask_login import login_required
from flask import render_template, Blueprint
from datetime import datetime
from app.models import Expense, Budget


charts = Blueprint('charts', __name__)

CURR_MONTH = datetime.now().strftime('%B')
MONTH_NUM = datetime.strptime(CURR_MONTH, '%B').month


@charts.route("/charts", methods=['GET', 'POST'])
@login_required
def chart_overview():

    # Define the labels for the x-axis
    months = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June',
              'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    # Generate income/budget lists of values from database
    monthly_amount = calculate_amount_spent(months)

    # Create grouped bars chart for monthly cash flow
    image_base64_bars = plot_bars_chart(monthly_amount, months)

    # Create the bar chart for the current-month's cash flow
    current_budget = Budget.query.filter_by(month=CURR_MONTH).first()
    if current_budget is None:
        current_budget = Budget(id=MONTH_NUM,
                                month=CURR_MONTH,
                                income=0,
                                budget=0,
                                left_cash=0, date_posted=datetime.now())
        db.session.add(current_budget)
        db.session.commit()
    else:
        # Calculate the difference between earned and spent
        image_base64_hor_bars = plot_horizontal_chart(
            current_budget.income, current_budget.budget, current_budget.left_cash)
        spending_amount = round_number(
            current_budget.income - current_budget.left_cash)
        amount_over = round_number(spending_amount - current_budget.budget)

    # Query the CSV expense file goruped by categories and sorted by amount
    query_expenses = generate_expenses(MONTH_NUM)
    # Converting the pandas dataframe to a dictionary
    amount_dict = query_expenses.set_index('Category')['Amount'].to_dict()

    # define a list of CSS colors
    colors = []
    # create a new dictionary with the same keys and empty lists as values
    new_dict = {key: [] for key in amount_dict}
    # populate the new dictionary with the values from the original dictionary as lists
    for key, value in amount_dict.items():
        color = generate_random_cl()
        new_dict[key].append(value)
        new_dict[key].append(color)
        colors.append(color)

    # Create Pie chart as breakdown expenses
    image_base64_pie = plot_pie_chart(amount_dict, colors)

    # # Pass the chart path and the grouped DataFrame to the template
    return render_template('charts.html', image_bars=image_base64_bars,
                           image_hor_bar=image_base64_hor_bars,
                           image_pie=image_base64_pie,
                           current_budget=current_budget,
                           amount_over=amount_over,
                           spending_amount=spending_amount,
                           data_dict=new_dict)
