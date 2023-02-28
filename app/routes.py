from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.Forms.form import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import pyotp


@app.route("/")
def main():
    return render_template('layout.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('login_2fa'))
            return redirect(url_for("login_2fa"))
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
