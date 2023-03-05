from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.Forms.form import RegistrationForm, LoginForm, UpdateAccountForm, ExpenseForm
from app.models import User, Expense
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
import pyotp


@app.route("/")
def main():
    expenses = Expense.query.all()
    return render_template('home.html', expenses=expenses)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # fake password created from the password input
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        # An alert function indicate the existing user
        flash(f'Account created for {form.username.data}!', 'success')
        # if the form is validated properly
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('login_2fa'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/login/2fa/")
def login_2fa():
    # getting secret key used by user
    secret = pyotp.random_base32()
    return render_template("two_factor_setup.html", secret=secret)


@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("main"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = form.new_password.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.new_password.data = current_user.image_file
    image_file = url_for(
        'static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/expense/add", methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        add = ExpenseForm(title=form.title.data, amount=form.amount.data,
                          date_spend=form.date_spend.data,
                          category=form.category.data,
                          merchant=form.content.data, user=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Your new expense has been created!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = 'Enter a description'
        form.amount.data = '$'
    return render_template('create_expense.html', title='New Expense', form=form, legend='New Expense')
