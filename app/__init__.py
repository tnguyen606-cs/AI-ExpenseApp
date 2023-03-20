# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
# from twilio.rest import Client
from app.config import Config

# take environment variables from .env.
load_dotenv()


# Set the database
db = SQLAlchemy()  # db intitialized here
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# TWILIO_ACCOUNT
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)


def create_app(config_class=Config):
    # __name__ === __main__ tells Flask where to look for at running
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.users.routes import users
    from app.expenses.routes import expenses
    from app.main.routes import head
    from app.budgets.routes import budgets
    app.register_blueprint(users)
    app.register_blueprint(expenses)
    app.register_blueprint(head)
    app.register_blueprint(budgets)

    return app
