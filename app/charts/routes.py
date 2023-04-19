from app.charts.utils import round_number, calculate_amount_spent, update_data_list, get_spending, get_month_expense, plot_saving_chart, plot_balance_chart, plot_bars_chart, plot_horizontal_chart, plot_pie_chart, plot_area_chart, generate_random_cl
from app import db
from app.models import Goal
from flask_login import login_required
from flask import render_template, Blueprint
from datetime import datetime, timedelta
from app.models import Budget


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

    # Create Balance Bar Chart
    image_base64_balance = plot_balance_chart(monthly_amount, months)

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

    # Query the CSV expense file to a dict, grouped by categories and sorted by amount
    amount_dict = get_month_expense(datetime(2023, MONTH_NUM, 1))
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

    # Generate date of 30 days period
    last_30_days = datetime.now() - timedelta(days=30)
    # Current Month
    spending = get_spending(last_30_days)
    current_month_list = spending['Amount'].tolist()
    current_month_list = update_data_list(
        current_month_list, current_month_list[0], current_month_list[-1])
    date_list = spending['Date Spend'].tolist()
    date_list = update_data_list(
        date_list, (date_list[0] - timedelta(days=1)), datetime.now())
    date_list = [date_list[i].strftime('%b %d') for i in range(len(date_list))]
    date_list[-1] = 'Today'
    # Last Month
    last_month = last_30_days - timedelta(days=30)
    # Create lists for the current and last month
    last_spent = get_spending(last_month)
    last_month_list = last_spent.loc[(
        last_spent['Date Spend'] < last_30_days)]['Amount'].tolist()
    last_month_list = update_data_list(
        last_month_list, last_month_list[0], last_month_list[-1])
    # Create Area chart
    image_base64_area = plot_area_chart(
        date_list, current_month_list, last_month_list)
    # Calculate the different between two months
    diff_spent = sum(last_month_list) - sum(current_month_list)

    # Create the Saving Pie Chart
    goal = Goal.query.first()
    total = goal.amount
    saving = goal.amount_saving
    target_date = goal.date_end.strftime('%B, %Y')
    image_base64_saving = plot_saving_chart(total, saving)

    # Pass the chart path and the grouped DataFrame to the template
    return render_template('charts.html', image_balance=image_base64_balance,
                           image_saving=image_base64_saving,
                           image_bars=image_base64_bars,
                           image_hor_bar=image_base64_hor_bars,
                           image_pie=image_base64_pie,
                           image_area=image_base64_area,
                           current_budget=current_budget,
                           amount_over=amount_over,
                           spending_amount=spending_amount,
                           data_dict=new_dict, diff_spent=diff_spent, total=total, saving=saving, target_date=target_date)
