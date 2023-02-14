from flask import Flask, render_template, url_for, flash, redirect
from Forms.form import RegistrationForm, LoginForm

# __name__ === __main__ tells Flask where to look for at running
app = Flask(__name__)

# Set a secret key for the app to prevent HACKERs
app.config['SECRET_KEY'] = '9bed793b88c55537107733b2340c652f'


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



# An Alternative Way to create a debug mode
if __name__ == '__main__':
    app.run(debug=True)
