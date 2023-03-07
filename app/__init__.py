# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_currency import Currency

# Initialize the app
# __name__ === __main__ tells Flask where to look for at running
app = Flask(__name__)

# test code
app.app_context().push()

# Set a secret key: a key used to secure the sessions that remember information from one request to another
app.config['SECRET_KEY'] = '9bed793b88c55537107733b2340c652f'

# Set SQLALCHEMY as config: The database URI specifies the database you want to establish a connection with using SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.db'

# Optional: A configuration to enable or disable tracking modifications of objects.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
currency = Currency(app, db)

# Load the views
from app import routes
from app import models
# No change
