- [Database setting, table populating](#database-setting-table-populating)
  - [Creating the database](#creating-the-database)
  - [Populating the table](#populating-the-table)
- [Displaying all records](#displaying-all-records)
  - [Creating a base template](#creating-a-base-template)
  - [Create an index.html template file](#create-an-indexhtml-template-file)
- [Displaying a single record](#displaying-a-single-record)
  - [Create a new route that renders a page for each individual student](#create-a-new-route-that-renders-a-page-for-each-individual-student)


# Database setting, table populating

Requirements: 
```shell
$ pip install Flask Flask-SQLALchemy

```

## Creating the database

Preliminary work: write up the `app.py` as demonstrated in this
[webpage](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application).

```
# Listing 1

$ export FLASK_APP=app
$ flask shell
```

This special shell runs commands in the context of your Flask application, so
that the Flask-SQLAlchemy functions you’ll call are connected to your
application (Listing 1).

Import the database object and the student model, and then run the
db.create_all() function to create the tables that are associated with your
models (Listing 2).

```
# Listing 2

>>> from app import db, Student
>>> db.create_all()
```

**NOTE** The db.create_all() function does not recreate or update a table if it already
exists. The solution is to delete all existing database tables with the
db.drop_all() function and then recreate them with the db.create_all() function
like so:

```
db.drop_all()
db.create_all()
```

This will apply the modifications you make to your models, but will also delete
all the existing data in the database. To update the database and preserve
existing data, you’ll need to use **schema migration**, which allows you to
modify your tables and preserve data.

## Populating the table

```shell
# Listing 3

$ flask shell
>>> from app import db, Student
>>> student_john = Student(firstname='john', lastname='doe',
>>>                        email='jd@example.com', age=23,
>>>                        bio='Biology student')
```

To add a student to your database, you’ll import the database object and the
Student model, and create an instance of the Student model, passing it student
data through keyword arguments (Listing 3).

```
>>> student_john
<student john>
>>> student_john.firstname
'john'
>>> student_john.bio
'Biology student'
```

Because this student has not been added to the database yet, its ID will be
None:

```
>>> print(student_john.id)
None
```

To add this student to the database, you’ll first need to add it to a **database
session**, which manages a database transaction. Add the student_john object to
the session using the db.session.add() method to __prepare__ it to be written to
the database. To commit the transaction and apply the change to database, use
the db.session.commit() method:

```
>>> db.session.add(student_john)
>>> db.session.commit()
```

Now that student John is added to the database, you can get its ID:

```
>>> print(student_john.id)
1
```

You can also use the db.session.add() method to edit an item in the database.
For example, you can modify the student’s email like so:

```
>>> student_john.email = 'john_doe@example.com'
>>> db.session.add(student_john)
>>> db.session.commit()
```

Add more students into the database (Listing 4):
```
# Listing 4

>>> sammy = Student(firstname='Sammy',
>>>                lastname='Shark',
>>>                email='sammyshark@example.com',
>>>                age=20,
>>>                bio='Marine biology student')
>>> 
>>> carl = Student(firstname='Carl',
>>>                lastname='White',
>>>                email='carlwhite@example.com',
>>>                age=22,
>>>                bio='Marine geology student')
>>> 
>>> db.session.add(sammy)
>>> db.session.add(carl)
>>> db.session.commit()
```

Query all the records in the student table using the query attribute with the
all() method
```
>>> Student.query.all()
[<Student john>, <Student Sammy>, <Student Carl>]
```

# Displaying all records
In this step, you’ll create a route and a template to display all the students
in the database on the index page.

```python
# Listing 5
# app.py

"""
Use Flask-SQLAlchemy to interact with database in a Flask application
"""

import os
# The Flask class to create a Flask application instance.
# The render_template function to render templates.
# The request object to handle requests.
# The url_for to construct URLs for routes.
from flask import Flask, render_template, request, url_for, redirect
# To create a database object that connects to your Flask application, allowing 
# you to create and manipulate tables using Python classes, objects, and 
# functions without needing to use the SQL language.
from flask_sqlalchemy import SQLAlchemy
# Import the func helper from the sqlalchemy.sql module to access SQL functions. 
from sqlalchemy.sql import func

# To construct a file path for your database.db database file
basedir = os.path.abspath(os.path.dirname(__file__))
# To create a Flask application instance.
app = Flask(__name__)
# The database URI to specify the database file you want to establish a 
# connection with.
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
# A configuration to enable or disable tracking modifications of objects.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create a database object using the SQLAlchemy class, passing the application 
# instance to connect your Flask application with SQLAlchemy.
db = SQLAlchemy(app)
# Declare the table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    #  Server sets the default value in the database when creating the
    #  table, so that default values are handled by the database rather than the
    #  model.
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    # Server sets the default value in the database when creating the
    # table, so that default values are handled by the database rather than the
    # model
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

```

You will create an index() view function using the app.route() decorator. In this
function, you query the database and get all the students using the Student
model with the query attribute, which allows you to retrieve one or more items
from the database using different methods. You use the all() method to get all
student entries in the database. You store the query result in a variable called
students and pass it to a template called index.html that you render using the
render_template() helper function. (Listing 5).

## Creating a base template
Before you create the index.html template file on which you’ll display the
existing students in the database, you’ll first create a base template, which
will have all the basic HTML code other templates will also use to avoid code
repetition. Then you’ll create the index.html template file you rendered in your
index() function. 

Create a templates directory, then open a new template called base.html:

```
$ mkdir templates
$ code templates/base.html
```

Add the following code inside the base.html file (Listing 6):

```html
<!--Listing 6-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %} {% endblock %} - FlaskApp</title>
    <style>
        .title {
            margin: 5px;
        }

        .content {
            margin: 5px;
            width: 100%;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }

        .student {
            flex: 20%;
            padding: 10px;
            margin: 5px;
            background-color: #f3f3f3;
            inline-size: 100%;
        }

        .bio {
            padding: 10px;
            margin: 5px;
            background-color: #ffffff;
            color: #004835;
        }

        .name a {
            color: #00a36f;
            text-decoration: none;
        }

        nav a {
            color: #d64161;
            font-size: 3em;
            margin-left: 50px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">FlaskApp</a>
        <a href="#">Create</a>
        <a href="#">About</a>
    </nav>
    <hr>
    <div class="content">
        {% block content %} {% endblock %}
    </div>
</body>
</html>
```

## Create an index.html template file

```
$ code templates/index.html
```

Add the following code to it:

```html
<!--index.html-->

{% extends 'base.html' %}

{% block content %}
    <h1 class="title">{% block title %} Students {% endblock %}</h1>
    <div class="content">
        {% for student in students %}
            <div class="student">
                <p><b>#{{ student.id }}</b></p>
                <b>
                    <p class="name">{{ student.firstname }} {{ student.lastname }}</p>
                </b>
                <p>{{ student.email }}</p>
                <p>{{ student.age }} years old.</p>
                <p>Joined: {{ student.created_at }}</p>
                <div class="bio">
                    <h4>Bio</h4>
                    <p>{{ student.bio }}</p>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}

```

You use a Jinja for loop in the line `{% for student in students %}` to go through
each student in the students variable that you passed from the index() view
function to this template.

While in your flask_app directory with your virtual environment activated, tell
Flask about the application (app.py in this case) using the FLASK_APP
environment variable. Then set the FLASK_ENV environment variable to development
to run the application in development mode and get access to the debugger.

```shell
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```
With the development server running, visit the following URL using your browser:
```
http://127.0.0.1:5000/
```

# Displaying a single record

Leave the development server running and open a new terminal window.

```shell
$ flask shell
>>> from app import db, Student
>>> Student.query.filter_by(firstname='sammy').first()
>>> Student.query.filter_by(id=3),first()
```

You can use the shorter get() method, which allows you to retrieve a specific
item using its primary key:

```shell
>>> Student.query.get(3)
```

## Create a new route that renders a page for each individual student

Add the following route at the end of the app.py:

```python
@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)
```

You use the route `'/<int:student_id>/'`, with int: being a converter that
converts the default string in the URL into an integer. And student_id is the
URL variable that will determine the student you’ll display on the page.

Create a student.html template file:

```python
<!--student.html-->
{% extends 'base.html' %}

{% block content %}
    <span class="title">
        <h1>{% block title %} {{ student.firstname }} {{ student.lastname }}{% endblock %}</h1>
    </span>
    <div class="content">
            <div class="student">
                <p><b>#{{ student.id }}</b></p>
                <b>
                    <p class="name">{{ student.firstname }} {{ student.lastname }}</p>
                </b>
                <p>{{ student.email }}</p>
                <p>{{ student.age }} years old.</p>
                <p>Joined: {{ student.created_at }}</p>
                <div class="bio">
                    <h4>Bio</h4>
                    <p>{{ student.bio }}</p>
                </div>
            </div>
    </div>
{% endblock %}
```

Use your browser to navigate to the URL for the second student:

```shell
http://127.0.0.1:5000/2
```