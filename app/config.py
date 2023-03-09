class Config:
    # Set a secret key: a key used to secure the sessions that remember information from one request to another
    SECRET_KEY = '9bed793b88c55537107733b2340c652f'
    # Set SQLALCHEMY as config: The database URI specifies the database you want to establish a connection with using SQLAlchemy.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user_info.db'
    # Optional: A configuration to enable or disable tracking modifications of objects.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
