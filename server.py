"""Server for medtracker app. """
import json
from datetime import datetime, timedelta, date
from re import M
from select import select
from time import strftime
from tracemalloc import start
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
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user



CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/userinfo.profile']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
app = Flask(__name__)
app.secret_key = "ruvndexfdm"
# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


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
#     date = "2022-05-23"
#     time = "09:00:00"
#     session['credentials'] = {
#     'token': credentials.token,
#     'refresh_token': credentials.refresh_token,
#     'token_uri': credentials.token_uri,
#     'client_id': credentials.client_id,
#     'client_secret': credentials.client_secret,
#     'scopes': credentials.scopes}
#     date = date
#     time = time
#     print(f"THE DATETIME IS ***** {date}T{time}")
#     event = {
#         'summary': 'MB',
#         'description': 'list_of_doses',
#         'start': {
#             'dateTime': f'{date}T{time}:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         'end': {'dateTime': f'{date}T{time}:59',
#                 'timeZone': 'America/Los_Angeles',
#         },
#         # 'recurrence': ['RRULE:FREQ=DAILY;COUNT=2'],
#     }
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     return jsonify(event)


@app.route('/authorize')
def authorize():
    """Authorizes Google Calendar"""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json', scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        included_grant_scopes = 'true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """Sets credentials"""
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
    return redirect('/schedule')

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

    # taken_short_term=request.form.get("series")
    # if taken_short_term:
    #     taken_short_term=True
    # else:
    #     taken_short_term=False

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
    
    # typical_time=request.form.get("timepicker")
    # if typical_time:
    #     typical_time = typical_time
    # else:
    #     typical_time=None

    med = Med.get_by_med_name(med_name)

    if med:
        med_id = med.med_id
        added_med = UserMed.create(user_id=user_id,
                                    med_id=med_id,
                                    taken_regularly=taken_regularly,
                                    taken_as_needed=taken_as_needed,
                                    # taken_short_term=taken_short_term,
                                    currently_taking=currently_taking,
                                    typical_dose=typical_dose,
                                    # typical_time=typical_time,
                                    last_updated_date=date.today(),
                                    last_updated_time=datetime.now().time())
        
    else:
        med = Med.create(med_name=med_name,
                                med_information = None,
                                official=False,
                                added_by = int(user_id))
        db.session.add(med)
        db.session.commit()
        med = Med.get_by_med_name(med_name)
        med_id = med.med_id
        added_med = UserMed.create(user_id=user_id,
                                    med_id=med_id,
                                    taken_regularly=taken_regularly,
                                    taken_as_needed=taken_as_needed,
                                    # taken_short_term=taken_short_term,
                                    currently_taking=currently_taking,
                                    typical_dose=typical_dose,
                                    # typical_time=typical_time,
                                    last_updated_date=date.today(),
                                    last_updated_time=datetime.now().time())

    db.session.add(added_med)
    db.session.commit()
    session.modified = True
    flash(f"{med.med_name} was added to your profile.")
    return redirect("/add")

@app.route('/change')
def change_meds():
    """Change Med Profile."""

    if "user" in session:
        user_id = int(session["user"])
        user = User.get_by_id(user_id)
        return render_template("change.html",
                                    user = user)
    else: 
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/change-med', methods=["POST"])
def update_med():
    """Change a medication on a user's profile"""

    usermed_id = request.form.get("med-to-update")
    usermed_id = int(usermed_id)

    taken_regularly=request.form.get("regular")
    if taken_regularly:
        taken_regularly=True
        UserMed.make_taken_regularly(usermed_id)
        # typical_time=request.form.get("timepicker")
        # if typical_time:
        #     print("TYPICAL TIMEEEE")
        #     print(typical_time)
        #     typical_time = typical_time
        #     UserMed.set_typical_time(usermed_id=usermed_id, typical_time=typical_time)

    else:
        taken_regularly=False
        UserMed.make_not_taken_regularly(usermed_id)
        Dose.cancel_upcoming_doses_by_usermed(usermed_id)

    taken_as_needed=request.form.get("as-needed")
    if taken_as_needed:
        taken_as_needed=True
        UserMed.set_taken_as_needed(usermed_id)

    else:
        taken_as_needed=False
        UserMed.set_not_taken_as_needed(usermed_id)

    currently_taking=request.form.get("current")
    if currently_taking:
        currently_taking=True
        UserMed.set_currently_taking(usermed_id)
    else:
        currently_taking=False
        UserMed.set_not_currently_taking(usermed_id)

    typical_dose=request.form.get("dose-amount")
    if typical_dose:
        typical_dose=str(typical_dose)
        UserMed.set_typical_dose(typical_dose=typical_dose, usermed_id=usermed_id)
    else:
        typical_dose=None
        UserMed.set_typical_dose(typical_dose=None, usermed_id=usermed_id)
    
    UserMed.update_last_updated(usermed_id)
    #delete future doses
    #reschedule future doses

    # #delete med from profile
    # old_med = crud.delete_med_from_user(user_id = user_id, med_id = med_id)
    db.session.commit()
    # session.modified = True
    # flash(f"med {med_id} has been removed.")

    # #delete all upcoming doses of that med from profile
    # doses_of_old_med = crud.delete_doses_of_med_from_user(user_id = user_id, med_id = med_id)
    return redirect("/change")


# @app.route('/remove-med', methods=["POST"])
# def remove_med():
#     """Remove a med from a user's profile"""
#     user_id = session["user"]
#     med_id = request.form.get("med-to-remove")
#     med_id = int(med_id)

#     #delete med from profile
#     old_med = crud.delete_med_from_user(user_id = user_id, med_id = med_id)
#     db.session.commit()
#     session.modified = True
#     flash(f"med {med_id} has been removed.")

#     #delete all upcoming doses of that med from profile
#     doses_of_old_med = crud.delete_doses_of_med_from_user(user_id = user_id, med_id = med_id)
#     return redirect("/schedule")

@app.route('/my-meds')
def view_dose_history():
    """View med list and dose history"""
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
        new_buddy = UserBuddy.create(user_id = user_id, buddy_id = buddy_id, primary_buddy = False)
        db.session.add(new_buddy)
        User.spend_points(user_id, 15)
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
    """Display page for user to log meds"""

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
                                    date=date.today(),
                                    time=datetime.now().time(),
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


@app.route('/add')
def display_add_med():
    """Display page for user to add medication to med list."""

    if "user" in session:
        user_id = int(session["user"])
        user = User.get_by_id(user_id)
        return render_template("add.html",
                                    user = user)
    else: 
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/schedule')
def schedule_med_page(): 
    """Display page for user to schedule meds"""

    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        user_doses = Dose.get_upcoming_by_user(user_id=user_id)
        as_needed = UserMed.as_needed_by_user(user_id=user_id)

        return render_template('schedule.html',
                                user = user,
                                user_doses = user_doses,
                                as_needed=as_needed)
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
    starting_date = request.form.get('date')
    print(f"**************out of the form, the starting_date is {starting_date} which is a {type(starting_date)} object")
    time = request.form.get('time')
    initial_count = request.form.get('repeat')
    try:
        initial_count = int(initial_count)
    except:
        initial_count = 1

    if initial_count <= 0:
        initial_count = 1
    elif initial_count >= 1:
        initial_count = initial_count
    else:
        initial_count = 1

    values = request.form.getlist('medfordose')
    starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
    
    meds = []
    for value in values:
        usermed = UserMed.get_by_user_and_med(user_id=user_id, med_id=value)
        med_name = usermed.med.med_name
        meds.append(med_name)


    count = initial_count
    while count > 0:
        for value in values:
            date = starting_date + timedelta(days=(count-1))
            date = date.strftime('%Y-%m-%d')
            usermed = UserMed.get_by_user_and_med(user_id=user_id, med_id=value)
            usermed_id=usermed.usermed_id
            new_dose = Dose.create(user_id=user_id,
            med_id=value,
            usermed_id=usermed_id,
            date=date,
            time=time,
            notes=None,
            amount=None,
            cancelled=False
            )
        count = count - 1

        db.session.add(new_dose)
    
    db.session.commit()
    session.modified = True
    if calendar:
        starting_date = starting_date.strftime('%Y-%m-%d')
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'V3', credentials=credentials)

        event = {
            'summary': 'MB',
            'description': f'{meds}',
            'start': {
                'dateTime': f'{starting_date}T{time}:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {'dateTime': f'{starting_date}T{time}:59',
                    'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [f'RRULE:FREQ=DAILY;COUNT={initial_count}'],
        }
        event = service.events().insert(calendarId='primary', body=event).execute()


    flash(f"Meds scheduled!")

    
    return redirect('/schedule')

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
                            'name': med.med.med_name,
                            'information': med.med.med_information,
                            'official': med.med.official,
                            'current': med.currently_taking})

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
                    # 'doses': userdoses,
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
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        return render_template('dressup.html', user=user)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/customize')
def customize():
    """Select a main buddy and customize."""
    if "user" in session:
        user_id = session["user"]
        user = User.get_by_id(user_id)
        return render_template('customize.html', user=user)
    else:
        flash(f"Looks like you need to log in!")
        return redirect("/")

@app.route('/process-customization]', methods=["POST"])
def process_customization():
    """Process the customization"""

    chosen_buddy = request.form.get("chosen-buddy")
    chosen_buddy = int(chosen_buddy)
    chosen_hat = request.form.getlist("chosen-hat")
    chosen_glasses = request.form.getlist("chosen-glasses")
    chosen_random = request.form.getlist("chosen-random")
    chosen_background = request.form.getlist("chosen-background")
    buddy_url = f"buddy{chosen_buddy}_{chosen_hat}_{chosen_glasses}_{chosen_random}_{chosen_background}"

    UserBuddy.update_url(chosen_buddy, buddy_url)
    return redirect("/customize")


@app.route('/choose-buddy', methods=["POST"])
def choose_buddy():
    """Choose a main buddy and dress them with accessories (REACT)"""
    user_id = session["user"]
    chosen_buddy = request.form.get("chosen-buddy")
    chosen_accessories = request.form.get("chosen-accessories")

    main_buddy = UserBuddy.make_primary_buddy(userbuddy_id=chosen_buddy)
    db.session.commit()
    flash("Your main buddy has been updated!")

    return render_template('/')



@app.route('/med-data')
def med_data():
    """Data for all official meds in the db"""

    official_meds = Med.get_official()
    official = []
    for med in official_meds:
        official.append({'name': med.med_name,
                        'info': med.med_information})

    if 'user' in session:
        try:
            user_id = session["user"]
            unofficial_meds=Med.get_unofficial_by_user(user_id)
            unofficial = []
            for med in unofficial_meds:
                unofficial.append({'name': med.med_name,
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