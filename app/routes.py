from flask import render_template, url_for, flash, redirect
from app import app, db
from app.Forms.form import RegistrationForm, LoginForm
# from app.models import User, Post


@app.route("/")
def main():
    return render_template('layout.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin2023' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # An alert function indicate the existing user
        flash(f'Account created for {form.username.data}!', 'success')
        # if the form is validated properly
        return redirect(url_for('main'))
    return render_template('register.html', title='Register', form=form)
