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
    # a = jsonify([1,3])
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user(user_id):
    """shows info about individual user."""

    # user_zipcode = db.session.query(User.zipcode).filter(User.user_id == user_id).one()[0]
    # user_age = db.session.query(User.age).filter(User.user_id == user_id)

    user = User.query.get(user_id)


    return render_template("user.html", user=user)

@app.route('/registration')
def display_registration_form():
    """displays registration form"""

    return render_template("registration_form.html")


@app.route('/registration', methods=['POST'])
def process_registration():
    """processes registration form"""

    email = request.form.get("email")
    password = request.form.get("password")

    email_status = User.query.filter(User.email == email).first()

    # Check to see if that email exists in DB.
    # If not, create user (add to DB).
    if email_status is None:
        user = User(email=email,
                    password=password)

        # Add to the session to be stored.
        db.session.add(user)

    else:
        flash("You've already registered with us.")
        return redirect("/login")

    db.session.commit()

    return redirect("/")


@app.route('/login')
def login_display():
    """display the login page"""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Process login info."""

    # Get form data from login.
    email = request.form.get("email")
    password = request.form.get("password")

    # Querying database for email taken from login form.
    user = User.query.filter(User.email == email).first()

    if user and user.password == password:
        user_id = user.user_id
        session['user_id'] = user_id
        flash("Successful login")
#trying to figure out how to get following redirect route to redirect to specific user id
        return redirect('/users/<int:user_id>')
    else:
        flash("Your email and/or password doesn't match our records")
        return redirect("/login")


@app.route('/logout')
def logout():
    """logs user out by removing user_id from session"""

    session.pop('user_id', None)
    flash("Successfully logged out")

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
