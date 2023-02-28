from flask import render_template, url_for, flash, redirect, request, session, abort
from app import app, db, bcrypt
from app.Forms.form import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import pyqrcode


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
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.verify_totp(form.token.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


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
        session['username'] = user.username
        flash('You need to scan the QR code below to complete registration')
        return redirect(url_for('two_factor_setup'))
    return render_template('register.html', title='Register', form=form)


@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('main'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('main'))
        # this page contains sensitive qr code
        # browser should not cache it
    return render_template('two_factor_setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # remove username from session for added security
    del session['username']

    # render qrcode from FreeOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
