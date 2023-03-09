from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, client
from datetime import datetime
from app.Forms.form import RegistrationForm, LoginForm, UpdateAccountForm, ExpenseForm
from app.models import User, Expense
from app.Helpers.helpers import send_sms_to, save_picture
import pyotp

@app.route("/")
def main():
    return render_template('main.html')


@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.order_by(Expense.date_spend.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', expenses=expenses)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # fake password created from the password input
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_pw, phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        # An alert function indicate the existing user
        flash(
            f'Account created for {form.username.data}, please login with your existing account!', 'success')
        # if the form is validated properly
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Find user by username entered.
        user = User.query.filter_by(username=login_form.username.data).first()
        # Check stored password hash against entered password hashed.
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            # This helps us login to the previous we just closed without a double-login-steps
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('login_2fa'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=login_form)


@app.route("/login/2fa/")
@login_required
def login_2fa():
    # getting secret key used by user
    secret = pyotp.random_base32()
    return render_template("two_factor_setup.html", secret=secret)


@app.route("/login/2fa/", methods=["POST"])
@login_required
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("home"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # If new password is updated
        if form.new_password.data:
            hashed_pw = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # Send account updated message via Twilio
        # phone="+{}".format(form.phone.data)
        message = client.messages.create(
            to=send_sms_to(), 
            from_="+18776647341",
            body="We noticed you just updated your account information!"
        )
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = send_sms_to()

    # Get the path of the image saves in database
    image_file = url_for(
        'static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)


@app.route("/expense/add", methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    today_date = datetime.now()
    if form.validate_on_submit():
        new_expense = Expense(title=form.title.data, amount=form.amount.data,
                              date_spend=form.date_spend.data,
                              category=form.category.data,
                              merchant=form.merchant.data,
                              user=current_user, date_posted=today_date)
        db.session.add(new_expense)
        db.session.commit()
        flash('Your new expense has been created!', 'success')
        message = client.messages.create(
            to=send_sms_to(), 
            from_="+18776647341",
            body="We noticed you just added a new expense with an amount of {}!".format(new_expense.amount)
        )
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.date_spend.data = today_date
    return render_template('create_expense.html', title='New Expense', form=form, legend='New Expense')


@app.route("/expense/<int:expense_id>")
@login_required
def expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense.html', title=expense.title, expense=expense)


@app.route("/expense/<int:expense_id>/update", methods=['GET', 'POST'])
@login_required
def expense_update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.date_spend = form.date_spend.data
        expense.category = form.category.data
        expense.merchant = form.merchant.data
        expense.date_posted = datetime.now()
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('expense', expense_id=expense.id))
    elif request.method == 'GET':
        form.title.data = expense.title
        form.amount.data = expense.amount
        form.date_spend.data = expense.date_spend
        form.category.data = expense.category
        form.merchant.data = expense.merchant
    return render_template('create_expense.html', title='Edit Expense',
                           form=form, legend='Edit Expense')


@app.route("/expense/<int:expense_id>/delete", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    message = client.messages.create(
            to=send_sms_to(), 
            from_="+18776647341",
            body="We noticed you just deleted an expense with an amount of {}!".format(expense.amount)
        )
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('home'))
