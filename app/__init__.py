# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from twilio.rest import Client
from app.config import Config


# Set the database
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# TWILIO_ACCOUNT
account_sid = 'AC26c8dffe2e5379741a1f8efc0f2ede4f'
auth_token = 'a3fc413ae20897ee7d492c1024f31e21'
client = Client(account_sid, auth_token)


def create_app(config_class=Config):
    # __name__ === __main__ tells Flask where to look for at running
    app = Flask(__name__)
    app.config.from_object(Config)

    # test code
    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.users.routes import users
    from app.expenses.routes import expenses
    from app.main.routes import head
    app.register_blueprint(users)
    app.register_blueprint(expenses)
    app.register_blueprint(head)

    return app
