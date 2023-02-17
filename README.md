<!-- PROJECT LOGO -->
<p align="center">

  <h1 align="center">AI-Expense Saving App</h3>

  <p align="center">
    An awesome AI-powered expense-saving app to jumpstart that helps users in saving little by little for personal goals by tracking users daily expenses and send summary alerts via SMS message. 
  </p>
  <br/>
  <p>
    Further, AI and ML are at the core of the App. Its AI and ML algorithms help the platform to deliver the tailored response based on users personal finances. For instance, one can even ask questions such as whether you have the budget to buy a particular product that should not hurt the target goal — the assistant will take a dive into the graphs and data-driven insights and would answer your queries. That is not all, its users can also set a limit of  spare changes on the App and the assistant will put that amount aside as users savings, which helps to improve users overall financial wellness.
  </p>
</p>

<br/>
<!-- DESIGN SYSTEM -->
<h2 align="center">DESIGN SYSTEM</h1>

<p align="center">To get a big picture of how I develop this app, this is a preliminary list of features for financial software solution. </p>
<br/>

### Key Features

This list includes: 
* **Registration/Log In**: Use `SSO` and `Google two-factor Authenticator` in `Python` to make sure that users’ log-in flow is secured and no unauthorized person can get into the account. Also, Single Sign-on (SSO) enables secure user authentication with one set of credentials to several applications. 
* **User profile**: Take care of personalization of user (e.g., Name, Email, Password, Phone, Location, ect.)
* **Tracking expenses**: The `data` for the expense report is taken from users inputs.
* **Financial Goals**: Provide a range of predefined goals covering options such as paying off credit card debt or savings, leaving users the chance to create their own goals.
* **Compliance**: Let users automate their savings by setting spending limits or automatically saving their spare change from daily purchases. 
* **Analytics and reports**: Display categories through visible `charts` that give users a detailed view (*Net Income Over Time Chart, Total Monthly Expenses Chart, Expenses Breakdown Chart*). Define all users transactions based on categories such as Income, Restaurant, Gas, ect. Use `PostgreSQL` for analytical processing and `Data Visualizaiton` with `Mathplotlib`.
* **Predict money flow**: As analyzing users financial situation, the app delivers financial suggestions when being asked that let users know where they can invest and increase capital. Use `AI` and `Machine learning` concepts in order to make decisions by feeding said data.
* **Notifications and alerts**: Users will receive SMS Transaction Notifications for their TransferWise Account with `Twilio API` and `Python`.
* **Deployments**: Heroku and AWS.
* **Agile automations**: Zenhub.

<br/>

### Resources

* [Understanding how a 2-factor authenticator works](https://blog.bytebytego.com/p/ep-16-design-google-placesyelp-also)
* [What is SSO](https://blog.bytebytego.com/p/what-is-sso-episode-7)
* [How to store Password safely in Database](https://www.youtube.com/watch?v=zt8Cocdy15c)
* [Why Python integrate with PostgreSQL](https://blog.bytebytego.com/p/ep30-why-is-postgresql-the-most-loved)
* [Matplotlib Data visualization](https://www.youtube.com/watch?v=UO98lJQ3QGI)
* [How to send sms notifications](https://www.twilio.com/blog/sms-transaction-notifications-transferwise-twilio-python)
* [Predicting Money Spending Direction using Support Vector Machines](https://jakevdp.github.io/PythonDataScienceHandbook/05.07-support-vector-machines.html)
* [Heroku Deployment](https://www.youtube.com/watch?v=6DI_7Zja8Zc&t=613s)

### Set-up Steps 

1. Set up enviroments: install [Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/) and Python
2. Run `export FLASK_DEBUG=1` to activate the active *Debug* mode on the browser or use `__name__` in file to reload page automatically
3. Run the app: `python flaskmain.py`
4. Get a *secret* key: Run `python` -> `import secrets` -> `secrets.token_hex(16)`
5. Fancy form library - *WTForms*. Ex, to use *TextField* with Form: Run `pip install flask-wtf`
6. 





