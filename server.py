"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, 
flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
    return a

@app.route('/users')
def user_list():
    """show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/registration')
def display_registration_form():
    """displays registration form"""

    return render_template("registration_form.html")


@app.route('/registration', methods=['POST'])
def process_registration():
    """processes registration form"""

    email = request.form.get("email")
    password = request.form.get("password")

    email_status = User.query.filter(User.email.in_(email)).all()

    #check to see if that email exists in our DB
    #if not, create user (add to DB)
    if email_status == []:
        user = User(email=email,
                    password=password)

        # Add to the session to be stored.
        db.session.add(user)

    else:
        print "You've already registered with us."

    db.session.commit()

    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    """"""

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
