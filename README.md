<!-- PROJECT LOGO -->
<p align="center">

  <h1 align="center">AI-Expense Saving App</h3>

  <p align="center">
    An awesome AI-powered expense-saving app to jumpstart that helps users in saving little by little for personal goals by managing and tracking users expenses and send summary alerts via SMS message. 
  </p>
  <br/>
  <p>
    Further, AI and ML are at the core of the App. Its AI and ML algorithms help the platform deliver tailored responses based on users personal finances. For instance, one can even ask questions such as whether I have the budget to buy a particular product that should not hurt the target goal — the assistant of the app will take a dive into the graphs and data-driven insights and would answer my queries. That is not all, the users can also set a limit of spare changes on the App and the app will put that amount aside as users savings, which helps to improve users overall financial wellness.
  </p>
</p>

<br/>
<!-- DESIGN SYSTEM -->
<h2 align="center">DESIGN SYSTEM</h2>

<p align="center">To get a big picture of how I develop this app, this is a preliminary list of features for financial software solution. </p>
<br/>

### Key Features

- **Registration/Log In**: Use **TOTP** and **Google Two-factor Authenticator** in _Python_ to make sure that users’ log-in flow is secured and no unauthorized person can get into the account. Also, **BCrypt Algorithm** is used to hash and save passwords securely.
- **User profile**: Take care of personalization of user (e.g., Name, Email, Password, ect.).
- **Tracking expenses**: The data for the expense report is taken from users inputs.
- **Financial Goals**: Provide a range of predefined goals covering options such as paying off credit card debt or savings, leaving users the chance to create their own goals.
- **Compliance**: Let users automate their savings by setting spending limits or automatically saving their spare change from daily purchases.
- **Analytics and reports**: Display categories through visible _charts_ that give users a detailed view (_Net Income Over Time Chart, Total Monthly Expenses Chart, Expenses Breakdown Chart_). Define all users transactions based on categories such as Income, Restaurant, Gas, ect. Use **PostgreSQL** for analytical processing and _Data Visualizaiton_ with **Mathplotlib**.
- **Predict money flow**: As analyzing users financial situation, the app delivers financial suggestions when being asked that let users know where they can invest and increase capital. Use **AI** and **Machine learning** concepts in order to make decisions by feeding said data.
- **Notifications and alerts**: Users will receive SMS Transaction Notifications for their TransferWise Account with **Twilio API** and **Python**.
- **Deployments**: Heroku and AWS.
- **Agile automations**: Zenhub.

<!-- TECH STACK -->
<br/>

### Tech Stack

1. Web framework: **Flask**
2. Storing User Data: **SQLAlchemy**
3. Database: **SQLLite** for testing and **PostgreSQL** for production

<!-- STEPS -->
<br/>
<h2 align="center">Set-up Steps</h2>

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

<!-- ZENHUB -->
<br/>
<h2 align="center">Progress</h2>

1. Created **Login/Register** pages
2. Set up a **Database** and Stored User Data with SQLAlchemy
3. Created **User Authentication** to keep passwords and information safe using `BCrypt Algorithm`
4. Implemented **TOTP 2FA** with **Google Authenticator** in Python and Flask
5. Created **User Account** and Profile picture where users can update their info
6. Created **Add Expense** option in navbar so that user can now add new expense

<br/>

### A top-level directory layout

```bash
    .
    ├── LICENSE
    ├── README.md
    ├── app
    │   ├── init.py       # Initialize the app
    │   ├── models.py     # Database's Models
    │   ├── routes.py     # List of routes
    │   └── templates
    │       ├── account.html
    │       ├── home.html
    │       ├── layout.html
    │       ├── login.html
    │       ├── register.html
    │       └── two_factor_setup.html
    │   ├── Forms
    │   │   ├── pycache
    │   │   │   └── form.cpython-37.pyc
    │   │   └── form.py
    │   ├── static
    │   │   └── main.css
    │   ├── instance
    │   │   └── site.db
    │   ├── pycache
    │   │   ├── init.cpython-37.pyc
    │   │   ├── models.cpython-37.pyc
    │   │   └── routes.cpython-37.pyc
    ├── instance
    │   └── user_info.db
    └── run.py
```

<br/>

### Resources

- [Understanding how a 2-factor authenticator works](https://blog.bytebytego.com/p/ep-16-design-google-placesyelp-also)
- [What is SSO](https://blog.bytebytego.com/p/what-is-sso-episode-7)
- [How to store Password safely in Database](https://www.youtube.com/watch?v=zt8Cocdy15c)
- [Why Python integrate with PostgreSQL](https://blog.bytebytego.com/p/ep30-why-is-postgresql-the-most-loved)
- [Matplotlib Data visualization](https://www.youtube.com/watch?v=UO98lJQ3QGI)
- [How to send sms notifications](https://www.twilio.com/blog/sms-transaction-notifications-transferwise-twilio-python)
- [Predicting Money Spending Direction using Support Vector Machines](https://jakevdp.github.io/PythonDataScienceHandbook/05.07-support-vector-machines.html)
- [Heroku Deployment](https://www.youtube.com/watch?v=6DI_7Zja8Zc&t=613s)
