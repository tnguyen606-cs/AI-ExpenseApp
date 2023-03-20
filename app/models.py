# CREATE TABLE
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


# Reloading user id from stored users so that the app can find user by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # id for each User
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # user has a unique default picture
    image_file = db.Column(db.String(50), nullable=False,
                           default='default.jpg')
    # pp can have same password
    password = db.Column(db.String(100), nullable=False)
    # phone number to use SMS message
    phone = db.Column(db.Integer, unique=True, nullable=False)
    # lazy=true means db created
    # This will act like a List of Expense objects attached to each User.
    # The "user" refers to the user property in the Expense/Budget class.
    expenses = db.relationship('Expense', backref='user', lazy=True)
    budget = db.relationship('Budget', backref='user', lazy=True)
    # backref is a shortcut for configuring both parent.children and child.parent relationships at one place only on the parent or the child class (not both).

    # Optional: this will allow each User object to be identified by its username,email,image when printed.
    def __repr__(self):
        return f"User('{ self.username}', '{ self.phone}', '{ self.password}'"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(precision=8, asdecimal=False,
                       decimal_return_scale=2), nullable=False)
    date_spend = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    merchant = db.Column(db.String(30), nullable=False)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # get the default time
    date_posted = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Expense {self.title}, {self.id}, {self.date_spend}, {self.date_posted}>'


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(precision=8, asdecimal=False,
                                  scale=2), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    date_end = db.Column(db.DateTime, nullable=False)
    period = db.Column(db.String(20), nullable=False)
    amount_saving = db.Column(db.Numeric(precision=8, asdecimal=False,
                                         scale=2), nullable=False, default=0.0)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # get the default time
    date_posted = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Budget {self.id}, {self.amount_saving}, {self.amount}>'
