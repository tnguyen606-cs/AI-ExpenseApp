# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

# Load the views
# No change
from app import routes
from app import models