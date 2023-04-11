from app.charts.utils import generate_categories, plot_bars_chart, plot_horizontal_chart, generate_top_expenses
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
    months_amount = generate_categories(months)

    # Create grouped bars chart display monthly cash flow
    image_base64 = plot_bars_chart(months_amount, months)

    # Create curr_month chart
    current_budget = Budget.query.filter_by(month=CURR_MONTH).first()
    if current_budget is None:
        current_budget = Budget(id=MONTH_NUM,
                                month=CURR_MONTH,
                                income=0,
                                budget=0,
                                left_cash=0, date_posted=datetime.now())
        db.session.add(current_budget)
        db.session.commit()

    # Create the bar chart for the cash flow
    if current_budget is not None:
        # Calculate the difference between earned and spent
        image_hor_base64 = plot_horizontal_chart(
            current_budget.income, current_budget.budget, current_budget.left_cash)

    # Query the CSV expense file
    query_exp_table = generate_top_expenses(2)

    # Converting the pandas dataframe to a dictionary
    data_dict = query_exp_table.set_index('Category')['Amount'].to_dict()
    top_data_dict = dict(list(data_dict.items())[0: 3])

    # # Pass the chart path and the grouped DataFrame to the template
    return render_template('charts.html', image_bars=image_base64,
                           image_hor_bar=image_hor_base64,
                           current_budget=current_budget,
                           data_dict=top_data_dict)
