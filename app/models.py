# CREATE TABLE
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
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
        return f"User('{ self.username}', '{ self.email}', '{ self.otp_secret}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  # get the default time
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}, {self.date_posted}>'


# Reloading user id from stored users so that the app can find user by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
