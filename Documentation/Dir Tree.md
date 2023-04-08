# A top-level directory structure

```bash
    .
    ├── LICENSE
    ├── run.py
    ├── app                     # The main Flask application directory
    │   ├── __init__.py         # A special file to make the app a package for imports to work properly
    │   ├── config.py
    │   ├── models.py           # The file that will contain Flask-SQLAlchemy models.
    │   ├── users               # The users blueprint for managing users
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   ├── routes.py
    │   │   └── utils.py
    │   ├── expenses            # The expenses blueprint of expenses
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   ├── routes.py
    │   │   └── utils.py
    │   ├── budgets             # The budgets blueprint of monthly budget
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   ├── routes.py
    │   │   └── utils.py
    │   ├── goals               # The goals blueprint of saving goal
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   ├── routes.py
    │   │   └── utils.py
    │   ├── main                # The main blueprint serving as the home page
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   │   ├── forms.py
    │   │   └── utils.py
    │   ├── static
    │   │   ├── images
    │   │   │   ├── 54b147f2e1c9f467.png
    │   │   │   ├── 78442eb9768a5147.png
    │   │   │   ├── 980c76b8223154fa.png
    │   │   │   └── a7d950e43d1cc7ad.png
    │   │   └── main.css
    │   ├── templates           # The templates directory contains files for all blueprints.
    │   │   ├── account.html
    │   │   ├── budget_update.html
    │   │   ├── budgets.html
    │   │   ├── create_budget.html
    │   │   ├── create_expense.html
    │   │   ├── create_goal.html
    │   │   ├── expense.html
    │   │   ├── goal_update.html
    │   │   ├── goals.html
    │   │   ├── home.html
    │   │   ├── layout.html
    │   │   ├── login.html
    │   │   ├── main.html
    │   │   ├── register.html
    │   │   └── two_factor_setup.html
    ├── instance
    │   ├── files
    │   │   ├── user_budgets.csv
    │   │   ├── user_expenses.csv
    │   │   └── user_goals.csv
    │   └── user_info.db
    ├── Documentation
    │   ├── Dir Tree.md
    │   ├── Flask-WTF.md
    │   ├── Retrieve DATA.md
    │   ├── SQLAlchemy.md
    │   └── Setup Process.md
    ├── Images
    │   ├── Database ER diagram.png
    │   └── expenses.gif
    └── LICENSE
```
