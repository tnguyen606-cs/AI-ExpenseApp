import os


class Config:
    # Set a secret key: a key used to secure the sessions that remember information from one request to another
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Set SQLALCHEMY as config: The database URI specifies the database you want to establish a connection with using SQLAlchemy.
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # Optional: A configuration to enable or disable tracking modifications of objects.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
