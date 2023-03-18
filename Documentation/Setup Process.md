## Set-up Steps

1. Install [Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/) and Python
2. Activate the active _Debug_ mode on the browser: Run `export FLASK_DEBUG=1` or use `__name__` in file to reload page automatically
3. Run the app: `python flaskmain.py`
4. Get a _secret_ key: Run `python` -> `import secrets` -> `secrets.token_hex(16)`
5. Get Fancy form library - _WTForms_. Ex, to use _TextField_ with Form: Run `pip install flask-wtf`
6. Install _SQLAlchemy_: Run `pip install flask-sqlalchemy`
7. Create DB: Run `db.create_all()`
8. Re-create DB: Run `db.drop_all()` and `db.create_all()`
9. Install _Bcrypt_: Run `pip install flask-bcrypt`
10. Install _User_ model: Run `from app import db` - `from app.models import User` - `User.query.all()` - `user`
11. Install user session management for Flask: `pip install flask-login`
12. Install the _PyOTP_ library : Run `pip install pyotp`
13. Install _Pillow?_ library to help reduce the image size: Run `pip install Pillow`
14. Install _Flask-Currency_ library, Currency handling extension for Flask and SQLAlchemy: Run `pip install FlaskCurrency`
14. Install [_Twilio_](https://www.twilio.com/docs/sms/quickstart/python): Run `pip install twilio`

### Resources

- [Understanding how a 2-factor authenticator works](https://blog.bytebytego.com/p/ep-16-design-google-placesyelp-also)
- [What is SSO](https://blog.bytebytego.com/p/what-is-sso-episode-7)
- [How to store Password safely in Database](https://www.youtube.com/watch?v=zt8Cocdy15c)
- [Why Python integrate with PostgreSQL](https://blog.bytebytego.com/p/ep30-why-is-postgresql-the-most-loved)
- [Matplotlib Data visualization](https://www.youtube.com/watch?v=UO98lJQ3QGI)
- [How to send sms notifications](https://www.twilio.com/blog/sms-transaction-notifications-transferwise-twilio-python)
- [Predicting Money Spending Direction using Support Vector Machines](https://jakevdp.github.io/PythonDataScienceHandbook/05.07-support-vector-machines.html)
- [Heroku Deployment](https://www.youtube.com/watch?v=6DI_7Zja8Zc&t=613s)
- [How to access environment variables from Python](https://www.twilio.com/blog/environment-variables-python)
