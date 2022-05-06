"""Server for medtracker app. """

from select import select
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Med, UserMed, Accessory, \
    UserAccessory, Buddy, UserBuddy, WearableBy, Dose
from jinja2 import StrictUndefined
from random import choice

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """View homepage."""
    try:
        user_id = session["user"]
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
    """Authenticate's user login"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.get_by_email(email)
    if not user or user.password != password:
        flash("Oops! You have entered an invalid email or password.")
    else:
        session["user"] = user.user_id
        session.modified = True
        print(session["user"])
        flash(f"Welcome back, {user.fname}!")

    return redirect("/profile")

@app.route("/logout", methods=["POST", "GET"])
def handle_logout():
    """Log out user"""
    session.pop('user', None)
    flash("See you next time!")
    return redirect("/")

# @app.route('/user/<User.user_id>')
# def show_user(user_id):
#     """Show a user's pets and inventory"""
#     return render_template('use')

@app.route('/profile')
def show_user():
    """Show a user's private profile information
    -points
    -pets
    -inventory
    -med schedule
    -med data"""

    if "user" in session:
        user_id = int(session["user"])
        print(f"the user_id is {user_id}")
        user = User.get_by_id(user_id)
        print(user.fname)
        print(user.meds)
        official_meds = Med.get_official()
    
        return render_template("profile.html",
                                    user = user,
                                    official_meds = official_meds)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")
    # elif session["user"]:
    #     user_id = session["user"]
    #     print(f"the user_id is {user_id}")
    #     
    #     print(f"the user is {user}")
    #     for med in user.meds:
    #         print(med.med_id)
    #     all_meds = Med.all_meds()
    #     print(all_meds)
    #     # # all_doses = Dose.get_by_user(user_id)
        # # print(all_doses)
        # # taken_doses = User.get_doses_taken(user_id)
        
@app.route('/adopt')
def view_adoption_page():
    """View adoption center"""
    buddies = Buddy.all_buddies()
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
    
        return render_template('adopt.html',
                                buddies = buddies,
                                user = user)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/add-buddy', methods=["POST"])
def add_buddy():
    """Add an adopted buddy to a user's profile"""
    #get information from a post request in profile.html
    #use the user's id and the med's id to add the med to the user
    
    user_id = session["user"]
    user = User.get_by_id(user_id)
    if user.points < 15:
        flash("Sorry! You don't have enough points for that buddy.")
    else:
        buddy_id = request.form.get("buddy-name")
        buddy = Buddy.get_by_id(buddy_id)
        new_buddy = crud.add_buddy_to_user(user_id = user_id, buddy_id = buddy_id)
        new_points = User.spend_points(user_id, 15)
        db.session.commit()
        flash(f"Welcome home, {buddy.buddy_name}. You'll love it here.")
        flash(f"{user.fname}, your new point total is {user.points}.")
        session.modified = True
    return redirect("/profile")

@app.route('/meds')
def view_all_meds():
    """View all meds in the database"""
    official_meds = Med.get_official()

    return render_template('meds.html',
                            official_meds = official_meds )


# @app.route('/meds/<med_id>')
# def view_med_details():
#     """View information about a particular medication"""
#     pass

@app.route('/add-med', methods=["POST"])
def add_med():
    """Add a med to a user's profile"""
    user_id = session["user"]
    print(f"the user is {user_id}")
    med_id = request.form.get("med-name")
    print(f"the med_id is {med_id}")
    if med_id == "select":
        new_med = request.form.get("other-med")
        print(f"new_med is {new_med}")
        new_med = Med.create(generic_name=new_med,
                                brand_name=new_med,
                                med_information = None,
                                official=False,
                                added_by = int(user_id))
        print(f"now new_med is {new_med}")
        db.session.add(new_med)
        print("new_med added to session")
        db.session.commit()
        print("and committed")
        new_med = Med.get_by_generic_name(new_med.generic_name)
        print(f"we got the generic name and now our newmed is {new_med}")
        med_id = new_med.med_id
        print(f"med_id is {med_id}")
        added_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)
        print("med added to user via function")
    else:
        new_med = Med.get_by_id(med_id)
        print(f"the new_med for else is {new_med}")
        added_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)
    print("after the loop")
    db.session.commit()
    print("new med committed to user db")
    session.modified = True
    flash(f"{new_med.generic_name} was added to your profile.")
    return redirect("/profile")
# @app.route('/remove-med', methods=["POST"])
# def add_med():
#     """Add a med to a user's profile"""
#     user_id = session["user"]
#     print(f"the user is {user_id}")
#     med_id = request.form.get("med-name")

#     print(f"the med they chose is {med_id}")
#     new_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)
#     flash(f"med {med_id} has been added to profile")
#     session.modified = True
#     return redirect("/profile")

@app.route('/log')
def log_med():
    """Log a medication to get points"""
    #select from scheduled doses
    #or put in a one-time med
    #get points
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)


        return render_template('log.html',
                                user = user)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/marketplace')
def view_marketplace():
    """View marketplace and go shopping"""
    accessories = Accessory.all_accessories()
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        if user.buddies:
            buddy = choice(user.buddies)
            
            return render_template('marketplace.html',
                                buddy = buddy,
                                user = user,
                                accessories = accessories)
        else: 
            flash("Looks like you need to adopt a buddy!")
            return redirect("/adopt")

    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/add-accessory', methods=["POST"])
def add_accessory():
    """Add a purchased accessory to a user's inventory"""
    #get information from a post request in profile.html
    #use the user's id and the med's id to add the med to the user
    
    accessory_id = request.form.get("accessory-name")
    accessory = Accessory.get_by_id(accessory_id)
    user_id = session["user"]
    user = User.get_by_id(user_id)

    if user.points < accessory.accessory_cost:
        flash("Sorry! You don't have enough points for that accessory yet. Keep saving!")
    else:
        new_accessory = crud.add_accessory_to_user(user_id = user_id, accessory_id = accessory_id)
        new_points = User.spend_points(user_id, accessory.accessory_cost)
        db.session.commit()
        flash(f"Ooh, what a nice new {accessory.accessory_name}!")
        flash(f"{user.fname}, your new point total is {user.points}.")
        session.modified = True
    return redirect("/marketplace")


# @app.route('/marketplace/<accessory_id>')
# def view_accessory():
#     """View information about a particular accessory in the marketplace"""
#     pass

# @app.route('/my_meds')
# def view_my_meds():
#     """Logged in users can view their private medication profile"""
#     pass

import crud

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
