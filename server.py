"""Server for medtracker app. """

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Med, UserMed, Accessory, \
    UserInventory, Buddy, UserBuddy, WearableBy, Dose
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """View homepage."""
    print('were home')
    return render_template('home.html')

@app.route("/users", methods=["POST"])
def create_new_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = User.get_by_email(email)

    if user:
        flash("A user is already registered with that email.")
    else:
        user = User.create(email, password, fname, lname=None)
        db.session.add(user)
        db.session.commit()
        flash("Account successfully created! Please log in.")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def handle_login():
    """Handles user login"""
    print('starting')
    email = request.form.get("email")
    print(f"the email is {email}")
    password = request.form.get("password")
    print(f"the password is {password}")
    user = User.get_by_email(2)
    #user = User.get_by_email(email)
    print(user)
    # if not user or user.password != password:
    #     flash("Oops! You have entered an invalid email or password.")
    # else:
    #     session["user_id"] = user.user_id
    #     flash("Login successful!")

    # return redirect("/")


# @app.route('/users/<user_id>')
# def show_user(user_id):
#     """Show a user's pets and inventory"""

@app.route('/profile')
def show_user(user_id):
    """Show a user's private profile information
    -all pets
    -all inventory
    -med schedule
    -med data
    -points
    -change account info"""

@app.route('/meds')
def view_all_meds():
    """View all meds in the database"""
    return render_template('meds.html')


# @app.route('/meds/<med_id>')
# def view_med_details():
#     """View information about a particular medication"""
#     pass

@app.route('/marketplace')
def view_marketplace():
    """View marketplace"""
    return render_template('marketplace.html')

# @app.route('/marketplace/<accessory_id>')
# def view_accessory():
#     """View information about a particular accessory in the marketplace"""
#     pass

# @app.route('/my_meds')
# def view_my_meds():
#     """Logged in users can view their private medication profile"""
#     pass

if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)
