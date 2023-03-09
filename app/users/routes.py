from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, client
from app.models import User
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.users.utils import send_sms_to, save_picture
import pyotp

users = Blueprint('users', __name__)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('head.main'))


@users.route("/register", methods=['GET', 'POST'])
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
        message = client.messages.create(
            to=send_sms_to(),
            from_="+18776647341",
            body="Welcome to the AI-Expense App!"
        )
        # An alert function indicate the existing user
        flash(
            f'Account created for {form.username.data}, please login with your existing account!', 'success')
        # if the form is validated properly
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Find user by username entered.
        user = User.query.filter_by(username=login_form.username.data).first()
        # Check stored password hash against entered password hashed.
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            # This helps us login to the previous we just closed without a double-login-steps
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.login_2fa'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=login_form)


@users.route("/login/2fa/")
@login_required
def login_2fa():
    # getting secret key used by user
    secret = pyotp.random_base32()
    return render_template("two_factor_setup.html", secret=secret)


@users.route("/login/2fa/", methods=["POST"])
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
        return redirect(url_for("head.home"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("users.login_2fa"))


@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = send_sms_to()

    # Get the path of the image saves in database
    image_file = url_for(
        'static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)
