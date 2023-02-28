# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the app
# __name__ === __main__ tells Flask where to look for at running
app = Flask(__name__)

# test code
app.app_context().push()

# Set a secret key for the app to prevent HACKERs
app.config['SECRET_KEY'] = '9bed793b88c55537107733b2340c652f'

# Set SQLALCHEMY as config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.db'

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Load the views
from app import models
from app import routes
# No change
