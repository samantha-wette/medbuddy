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
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json', scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        included_grant_scopes = 'true'
    )
    print(f"the state from google is {state} ***********************")
    session['state'] = state
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
    med_name = request.form.get("search")

    taken_regularly=request.form.get("regular")
    if taken_regularly:
        taken_regularly=True
    else:
        taken_regularly=False

    taken_short_term=request.form.get("series")
    if taken_short_term:
        taken_short_term=True
    else:
        taken_short_term=False

    taken_as_needed=request.form.get("as-needed")
    if taken_as_needed:
        taken_as_needed=True
    else:
        taken_as_needed=False

    currently_taking=request.form.get("current")
    if currently_taking:
        currently_taking=True
    else:
        currently_taking=False

    typical_dose=request.form.get("dose-amount")
    if typical_dose:
        typical_dose=str(typical_dose)
    else:
        typical_dose=None
    med = Med.get_by_generic_name(med_name)
    if med:
        med_id = med.med_id
        added_med = UserMed.create(user_id=user_id,
                                    med_id=med_id,
                                    taken_regularly=taken_regularly,
                                    taken_as_needed=taken_as_needed,
                                    taken_short_term=taken_short_term,
                                    currently_taking=currently_taking,
                                    typical_dose=typical_dose)
        
    else:
        med = Med.create(generic_name=med_name,
                                brand_name=None,
                                med_information = None,
                                official=False,
                                added_by = int(user_id))
        db.session.add(med)
        db.session.commit()
        med = Med.get_by_generic_name(med_name)
        med_id = med.med_id
        added_med = UserMed.create(user_id=user_id,
                                    med_id=med_id,
                                    taken_regularly=taken_regularly,
                                    taken_as_needed=taken_as_needed,
                                    taken_short_term=taken_short_term,
                                    currently_taking=currently_taking,
                                    typical_dose=typical_dose)
    db.session.add(added_med)
    db.session.commit()
    session.modified = True
    flash(f"{med.generic_name} was added to your profile.")
    return redirect("/med_profile")


@app.route('/remove-med', methods=["POST"])
def remove_med():
    """Remove a med from a user's profile"""
    user_id = session["user"]
    med_id = request.form.get("med-to-remove")
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
    
    user_id = session["user"]
    user = User.get_by_id(user_id)
    if user.points < 15:
        flash("Sorry! You don't have enough points for that buddy.")
    else:
        buddy_id = request.form.get("buddy-id")
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

    official_meds = Med.get_official()
    return render_template('meds.html',
                            official_meds = official_meds )


@app.route('/log')
def log_med(): 
    """Go to page to log medications"""

    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        user_doses = Dose.get_upcoming_by_user(user_id=user_id)
        as_needed = UserMed.as_needed_by_user(user_id=user_id)

        return render_template('log.html',
                                user = user,
                                user_doses = user_doses,
                                as_needed=as_needed)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/med-taken', methods=["POST"])
def med_taken():
    """Log a medication to get points"""
    user_id = session["user"]
    date_time = request.form.get('datetime')
    if not date_time:
        date_time = datetime.now()
    dose_ids = request.form.getlist('dose-id')
    med_ids = request.form.getlist('med-id')
    if med_ids:
        for med_id in med_ids:
            notes = request.form.get(f'notes-{med_id}')
            amount = request.form.get(f'amount-{med_id}')
            usermed = UserMed.get_by_user_and_med(user_id=user_id, med_id=med_id)
            usermed_id=usermed.usermed_id
            new_dose = Dose.create(user_id=user_id,
                                    med_id=med_id,
                                    usermed_id=usermed_id,
                                    date_time=date_time,
                                    time_taken=date_time,
                                    taken=True,
                                    notes=notes,
                                    amount=amount)
            db.session.add(new_dose)
            User.earn_points(user_id=user_id, num=1)

    if dose_ids:
        for dose_id in dose_ids:
            notes = request.form.get(f'notes-{dose_id}')
            amount = request.form.get(f'amount-{dose_id}')
            Dose.mark_taken(dose_id=dose_id,
                            time_taken=date_time,
                            notes=notes,
                            amount=amount)
            User.earn_points(user_id=user_id, num=1)
    
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
        if not session.get('credentials'):
            flash("Please authorize MedBuddy with Google Calendar and try again.")
            return redirect('/authorize')

    user_id = session["user"]
    datetime = request.form.get('datetime')
    values = request.form.getlist('medfordose')
    meds = []
    for value in values:
        usermed = UserMed.get_by_user_and_med(user_id=user_id, med_id=value)
        usermed_id=usermed.usermed_id
        meds.append(value)
        new_dose = Dose.create(user_id=user_id,
        med_id=value,
        usermed_id=usermed_id,
        date_time = datetime,
        notes=None,
        amount=None
        )
        db.session.add(new_dose)
    db.session.commit()
    session.modified = True
    if calendar:
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'V3', credentials=credentials)

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

@app.route('/manage')
def manage():
    """Render page for a user to manage their medications"""
    if 'user' in session:
        return render_template('manage.html')

    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/learn')
def learn():
    """Render page for user to learn about their meds"""
    if 'user' in session:
        return render_template('learn.html')

    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")
        

@app.route('/data')
def data():
    """Data for the user that is in session"""
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        fname = user.fname
        lname = user.lname
        id = user.user_id
        email = user.email
        password = user.password
        points = user.points
        img = '#'
        userbuddies = []
        for buddy in user.buddies:
            userbuddies.append({'id': buddy.buddy_id,
                                            'name': buddy.buddy_name,
                                           'description': buddy.buddy_description,
                                            'img': buddy.buddy_img,
                                            'alt': buddy.buddy_alt})
        useraccessories = []
        for accessory in user.accessories:
            useraccessories.append({'id': accessory.accessory_id,
                                                        'name': accessory.accessory_name,
                                                        'description': accessory.accessory_description,
                                                        'img': accessory.accessory_img,
                                                        'alt': accessory.accessory_alt,
                                                        'cost': accessory.accessory_cost
                                                     })
        usermeds = []
        for med in user.usermeds:
            usermeds.append({'id': med.med.med_id,
                            'name': med.med.generic_name,
                            'information': med.med.med_information,
                            'official': med.med.official,
                            'current': med.currently_taking})

        userdoses = []
        for dose in user.doses:
            userdoses.append({ 'dose_id': dose.dose_id,
                                        'med_id': dose.med_id,
                                        'med_name': dose.med.generic_name,
                                        'med_info': dose.med.med_information,
                                        'date_time': dose.date_time,
                                        'taken': dose.taken,
                                        'time_taken': dose.time_taken
                                        })
        user_dict = {
                    'id': id,
                    'fname' : fname,
                    'lname': lname,
                    'email': email,
                    'password': password,
                    'points': points,
                    'buddies': userbuddies,
                    'accessories': useraccessories,
                    'meds': usermeds,
                    'doses': userdoses,
                    'img': img
                    }
        return user_dict

    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/selector')
def selector():
    return render_template('med_selector.html')

@app.route('/dressup')
def dressup():
    """View dressup page."""

    return render_template('dressup.html')



@app.route('/med-data')
def med_data():
    """Data for all official meds in the db"""

    official_meds = Med.get_official()
    official = []
    for med in official_meds:
        official.append({'name': med.generic_name,
                        'info': med.med_information})

    if 'user' in session:
        try:
            user_id = session["user"]
            unofficial_meds=Med.get_unofficial_by_user(user_id)
            unofficial = []
            for med in unofficial_meds:
                unofficial.append({'name': med.generic_name,
                                    'info': med.med_information})
        except:
            unofficial = None

    all_meds = {'official': official,
                'unofficial': unofficial}
                
    return all_meds

import crud

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run("localhost", "5000", debug=True)