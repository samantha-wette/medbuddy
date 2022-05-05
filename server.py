"""Server for medtracker app. """

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Med, UserMed, Accessory, \
    UserInventory, Buddy, UserBuddy, WearableBy, Dose
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """View homepage."""
    try:
        user_id = session["user_id"]
        user = User.get_by_id(user_id)
    except: 
        user = None
    return render_template('home.html', user = user)

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
        user = User.create(email = email,
                            password = password,
                            fname = fname,
                            lname=lname)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome to MedBuddy, {user.fname}! Please log in.")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def handle_login():
    """Handles user login"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.get_by_email(email)
    if not user or user.password != password:
        flash("Oops! You have entered an invalid email or password.")
    else:
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.fname}!")

    return redirect("/profile")

# @app.route('/user/<User.user_id>')
# def show_user(user_id):
#     """Show a user's pets and inventory"""
#     return render_template('use')

@app.route('/profile')
def show_user():
    """Show a user's private profile information
    -all pets
    -all inventory
    -med schedule
    -med data
    -points
    -change account info"""
    
    try:
        user_id = session["user_id"]
        print(f"the user_id is {user_id}")
        user = User.get_by_id(user_id)
        print(f"the user is {user}")
        for med in user.meds:
            print(med.med_id)
        all_meds = Med.all_meds()
        print(all_meds)
        # # all_doses = Dose.get_by_user(user_id)
        # # print(all_doses)
        # # taken_doses = User.get_doses_taken(user_id)
        return render_template("profile.html",
                                    user = user,
                                    all_meds = all_meds)
    except:
        flash(f"Looks like you need to log in!")
        return redirect("/")



@app.route('/meds')
def view_all_meds():
    """View all meds in the database"""
    all_meds = Med.all_meds()

    return render_template('meds.html',
                            all_meds = all_meds )


# @app.route('/meds/<med_id>')
# def view_med_details():
#     """View information about a particular medication"""
#     pass

@app.route('/add-med', methods=["POST"])
def add_med():
    """Add a med to a user's profile"""
    #get information from a post request in profile.html
    #use the user's id and the med's id to add the med to the user
    
    user_id = session["user_id"]
    print(f"the user is {user_id}")
    med_id = request.form.get("med-name")

    print(f"the med they chose is {med_id}")
    new_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)
    flash(f"med {med_id} has been added to profile")
    return redirect("/profile")



@app.route('/log')
def log_med():
    """Log a medication to get points"""
    return render_template('log.html')

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
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
