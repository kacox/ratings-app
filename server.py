"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


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
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def register_form():
    """Show registration form."""
    return render_template("register_form.html")


@app.route('/register-process', methods=["POST"])
def process_form():
    """Process user registration information."""

    # get user name and email from POST request

    email = request.form.get("user_email")
    password = request.form.get("user_pass")

    if db.session.query(User).filter(User.email == email).first():
        # email does exist; send them to log in page
        flash("You already have an account.")
        return redirect("/")
    else:
        # email not in db yet; create new user in database
        db.session.add(User(email=email, password=password))
        db.session.commit()
        flash("Your account has been created.")
        return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
