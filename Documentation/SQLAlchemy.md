# Understanding

As you've seen, writing SQL commands are complicated and error-prone. It would be much better if we could just write Python code and get the compiler to help us spot typos and errors in our code. That's why SQLAlchemy was created.

SQLAlchemy is defined as an _ORM Object Relational Mapping library_. This means that it's able to map the relationships in the database into Objects. Fields become Object properties. Tables can be defined as separate Classes and each row of data is a new Object. This will make more sense after we write some code and see how we can create a Database/Table/Row of data using SQLAlchemy.

1. Comment out all the existing code where we create an SQLite database directly using the sqlite3 module.
2. Install the required packages flask and flask_sqlalchemy and import the Flask and SQLAlchemy classes from each.

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
```

HINT 1: The URL for your database should be `"sqlite:///[name of the database table].db"`

HINT 2: Don't if you get a deprecation warning in the console that's related to SQL_ALCHEMY_TRACK_MODIFICATIONS

You can silence it with `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`

HINT 3: You can always check the database using DB Browser.

# CRUD Operations

In addition to these things, the most crucial thing to figure out when working with any new database technology is how to CRUD data records.

**Create**

**Read**

**Update**

**Delete**

_So, let's go through each of these using SQLite and SQLAlchemy:_

### Create A New Record

```
new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
db.session.add(new_book)
db.session.commit()
```

### Read All Records

`all_books = session.query(Book).all()`

### Read A Particular Record By Query

`book = Book.query.filter_by(title="Harry Potter").first()`

### Update A Particular Record By Query

```
book_to_update = Book.query.filter_by(title="Harry Potter").first()
book_to_update.title = "Harry Potter and the Chamber of Secrets"
db.session.commit()
```

### Update A Record By PRIMARY KEY

```
book_id = 1
book_to_update = Book.query.get(book_id)
book_to_update.title = "Harry Potter and the Goblet of Fire"
db.session.commit()
```

### Delete A Particular Record By PRIMARY KEY

```
book_id = 1
book_to_delete = Book.query.get(book_id)
db.session.delete(book_to_delete)
db.session.commit()
```

You can also delete by querying for a particular value e.g. by title or one of the other properties.
