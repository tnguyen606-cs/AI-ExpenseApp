from flask import render_template, request, Blueprint
from flask_login import login_required
from app.models import Expense

head = Blueprint('head', __name__)


@head.route("/")
def main():
    return render_template('main.html')


@head.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.order_by(
        Expense.date_spend.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', expenses=expenses)
