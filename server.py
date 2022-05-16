"""Server for medtracker app. """

import json
from datetime import datetime, timedelta
from re import M
from select import select
from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for, make_response
from pyparsing import commonHTMLEntity
from model import  connect_to_db, db, User, Med, UserMed, Accessory, \
    UserAccessory, Buddy, UserBuddy, WearableBy, Dose
from jinja2 import StrictUndefined
from random import choice
# from authlib.integrations.flask_client import OAuth
import requests
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import hashlib
from googleapiclient.errors import HttpError

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/userinfo.profile']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
app = Flask(__name__)
app.secret_key = "ruvndexfdm"

@app.route('/')
def home():
    """View homepage."""
    try:
            user_id = session["user"]
            user = User.get_by_id(user_id)
    except:
            user = None
    
    return render_template('home.html', user = user)

@app.route('/search', methods=['POST'])
def search():
    """Searches for meds in autocomplete"""
    term = request.form['q']
    print ('term: ', term)
    
    file = open('static/data/meds.json', 'r')
    json_data = json.load(file)
    dict_of_dicts = json.loads(json_data)
    all_meds = []
    filtered_dict = []
    for dict in dict_of_dicts:
        all_meds.append(dict_of_dicts[dict]["name"])
    for med in all_meds:
        if term.lower() in med.lower():
            filtered_dict.append(med)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp

# @app.route('/test')
# def add_to_calendar():
#     print("*********HELLO*******")

#     print(session['credentials'])
#     if 'credentials' not in session:
#         return redirect('/authorize')
    
#     credentials = google.oauth2.credentials.Credentials(**session['credentials'])
#     print(credentials)


#     service = googleapiclient.discovery.build('calendar', 'V3', credentials = credentials)
#     print(f"the service is {service} *********")
    
#     session['credentials'] = {
#     'token': credentials.token,
#     'refresh_token': credentials.refresh_token,
#     'token_uri': credentials.token_uri,
#     'client_id': credentials.client_id,
#     'client_secret': credentials.client_secret,
#     'scopes': credentials.scopes}
#     datetime = "2022-05-14T11:54"
#     print(f"THE DATETIME IS ***** {datetime}")
#     event = {
#         'summary': 'MB',
#         'description': 'list_of_doses',
#         'start': {
#             'dateTime': f'{datetime}:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         'end': {'dateTime': f'{datetime}:59',
#                 'timeZone': 'America/Los_Angeles',
#         },
#         # 'recurrence': ['RRULE:FREQ=DAILY;COUNT=2'],
#     }
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     return jsonify(event)


@app.route('/authorize')
#make sure to do a redirect
def authorize():
    # state = hashlib.sha256(os.urandom(1024)).hexdigest()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json', scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        # state= state,
        included_grant_scopes = 'true'
    )
    print(f"the state from google is {state} ***********************")
    session['state'] = state

    # google = oauth.create_client('google')
    # redirect_uri = url_for('authorize', _external=True)
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes = SCOPES, state = state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes}
    print(session['credentials'])
    return redirect('/med_profile')

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

    return redirect("/")

@app.route("/logout", methods=["POST", "GET"])
def handle_logout():
    """Log out user"""
    for key in list(session.keys()):
        session.pop(key)
    flash("See you next time!")
    return redirect("/")

@app.route('/add-med', methods=["POST"])
def add_med():
    """Add a med to a user's profile"""
    user_id = session["user"]
    print(f"the user is {user_id}")
    med_name = request.form.get("search")
    new_med = Med.get_by_generic_name(med_name)
    if new_med:
        med_id = new_med.med_id
        added_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)

    else:
        new_med = Med.create(generic_name=med_name,
                                brand_name=None,
                                med_information = None,
                                official=False,
                                added_by = int(user_id))
        db.session.add(new_med)
        db.session.commit()
        new_med = Med.get_by_generic_name(med_name)
        med_id = new_med.med_id
        added_med = crud.add_med_to_user(user_id = user_id, med_id = med_id)
    print("after the loop")
    db.session.commit()
    print("new med committed to user db")
    session.modified = True
    flash(f"{new_med.generic_name} was added to your profile.")
    return redirect("/med_profile")

@app.route('/remove-med', methods=["POST"])
def remove_med():
    """Remove a med from a user's profile"""
    user_id = session["user"]
    med_id = request.form.get("med-to-remove")
    print(f"THE MED_ID IS HEREEEEEE {med_id}")
    med_id = int(med_id)

    #delete med from profile
    old_med = crud.delete_med_from_user(user_id = user_id, med_id = med_id)
    db.session.commit()
    session.modified = True
    flash(f"med {med_id} has been removed.")

    #delete all upcoming doses of that med from profile
    doses_of_old_med = crud.delete_doses_of_med_from_user(user_id = user_id, med_id = med_id)
    return redirect("/med_profile")


@app.route('/dose-history')
def view_dose_history():
    """View dose history"""
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        user_doses = Dose.get_by_user(user_id)
        doses_taken = Dose.get_taken_by_user(user_id)
        doses_missed = Dose.get_missed_by_user(user_id=user_id)
        return render_template('dose_history.html',
                                user = user,
                                doses_taken = doses_taken,
                                doses_missed = doses_missed)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

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
    return redirect("/")

@app.route('/meds')
def view_all_meds():
    """View all meds in the database"""

    # query = f"https://api.fda.gov/drug/drugsfda.json?api_key={FDA_API_KEY}&search=products.brand_name:'NAME'"


    official_meds = Med.get_official()


    return render_template('meds.html',
                            official_meds = official_meds )


@app.route('/log')
def log_med(): 
    """Go to page to log medications"""
    #select from scheduled doses
    #or put in a one-time med
    #get points
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        user_doses = Dose.get_upcoming_by_user(user_id=user_id)

        return render_template('log.html',
                                user = user,
                                user_doses = user_doses)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/med-taken', methods=["POST"])
def med_taken():
    """Log a medication to get points"""
    print("********* DOSES BEING LOGGED*********")
    user_id = session["user"]
    print(f"THE USER IS {user_id}")
    datetime = request.form.get('datetime')
    print(f"THE DATETIME IS {datetime} ************")
    dose_ids = request.form.getlist('dose-id')
    print(f"THE DOSEIDS ARE {dose_ids} *******")
    for dose_id in dose_ids:
        print(f"ITERATING, THIS DOSE_ID IS {dose_id}")
        taken_dose = Dose.mark_taken(dose_id=dose_id, time_taken=datetime)
        # db.session.add(taken_dose)
        print(f"THE DOSE HAS BEEN MARKED AS TAKEN")
        earned_points = User.earn_points(user_id=user_id, num=1)
        print(f"THE USER HAS MORE POINTS NOW!")
        # db.session.add(earned_points)
        # print("THE EARNED POINTS HAVE BEEN ADDED TO THE SESSION")
    db.session.commit()
    session.modified = True
    user_points = User.get_points(user_id=user_id)
    flash(f"Nice! You now have {user_points} points!")
    return redirect('/log')


@app.route('/med_profile')
def schedule_doses():
    """Schedule doses using meds on med list."""

    if "user" in session:
        user_id = int(session["user"])
        user = User.get_by_id(user_id)
        return render_template("med_profile.html",
                                    user = user)
    else: 
        flash(f"Looks like you need to log in!")
        return redirect("/")


@app.route('/add-dose', methods=["POST"])
def add_dose():
    """Add a dose to a user's profile"""

    calendar = request.form.get("calendar")
    if calendar:
        # try:
        #     credentials = session[credentials]
        # except:
        if not session.get('credentials'):
            flash("Please authorize MedBuddy with Google Calendar and try again.")
            return redirect('/authorize')

        #     credentials = session[credentials]
        #     print(credentials)
        #     print("**********")
        # else:

    user_id = session["user"]
    datetime = request.form.get('datetime')
    print(f"THE DATETIME IS {datetime} *****************************")
    values = request.form.getlist('medfordose')
    meds = []
    for value in values:
        meds.append(value)
        new_dose = Dose.create(user_id=user_id,
        med_id=value,
        date_time = datetime)
        db.session.add(new_dose)
    db.session.commit()
    session.modified = True
    if calendar:
        print(session['credentials'])        
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        print(credentials)
        service = googleapiclient.discovery.build('calendar', 'V3', credentials=credentials)
        print(service)

        event = {
            'summary': 'MB',
            'description': f'{meds}',
            'start': {
                'dateTime': f'{datetime}:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {'dateTime': f'{datetime}:59',
                    'timeZone': 'America/Los_Angeles',
            },
            # 'recurrence': ['RRULE:FREQ=DAILY;COUNT=2'],
        }
        event = service.events().insert(calendarId='primary', body=event).execute()


    flash(f"Meds scheduled!")

    
    return redirect('/med_profile')

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
            buddy = None
            return render_template('marketplace.html',
                                buddy = buddy,
                                user = user,
                                accessories = accessories)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/add-accessory', methods=["POST"])
def add_accessory():
    """Add a purchased accessory to a user's inventory"""
    #get information from a post request in profile.html
    #use the user's id and the med's id to add the med to the user
    
    accessory_id = request.form.get("accessory-id")
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

import crud

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run("localhost", "5000", debug=True)