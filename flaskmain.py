from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from Forms.form import RegistrationForm, LoginForm

# __name__ === __main__ tells Flask where to look for at running
app = Flask(__name__)

app.app_context().push()  # test code

# Set a secret key for the app to prevent HACKERs
app.config['SECRET_KEY'] = '9bed793b88c55537107733b2340c652f'

# Set SQLALCHEMY as config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the database
db = SQLAlchemy(app)

# CREATE TABLE


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id for each User
    username = db.Column(db.String(21), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # user has a unique default picture
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    # pp can have same password
    password = db.Column(db.String(60), nullable=False)
    # lazy=true means db created
    posts = db.relationship('Post', backref='author', lazy=True)

    # Optional: this will allow each User object to be identified by its username,email,image when printed.
    def __repr__(self):
        return f"User('{ self.username}', '{ self.email}', '{ self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  # get the default time
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}, {self.date_posted}>'


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
