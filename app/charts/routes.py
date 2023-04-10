from app.charts.utils import generate_categories, plot_bars_chart
from flask_login import login_required
from flask import render_template, Blueprint


charts = Blueprint('charts', __name__)


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

    # # Pass the chart path and the grouped DataFrame to the template
    return render_template('charts.html', image=image_base64)
