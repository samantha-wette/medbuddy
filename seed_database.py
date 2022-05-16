import os
import json
from random import choice, randint, random, randrange
from datetime import datetime
from venv import create
import model
import server

os.system("dropdb medtracker")
os.system("createdb medtracker")

model.connect_to_db(server.app)
model.db.create_all()

def create_buddies():
#create 5 buddies and store them in a list
    buddies_in_db = []
    for n in range(5):
        buddy_name = f"buddy{n}"
        buddy_description = f"a cool friend called {n}"
        buddy_img = "static/img/cat1.png"
        buddy_alt = "description of image"

        buddy=model.Buddy.create(buddy_name, buddy_description, buddy_img, buddy_alt)
        buddies_in_db.append(buddy)
    model.db.session.add_all(buddies_in_db)
    model.db.session.commit()

def create_meds():
    meds_in_db = []
    file = open('static/data/meds.json', 'r')
    json_data = json.load(file)
    dict_of_dicts = json.loads(json_data)
    for dict in dict_of_dicts:
        generic_name = (dict_of_dicts[dict]["name"])
        med_information = (dict_of_dicts[dict]["info"])
        med=model.Med.create(generic_name=generic_name, brand_name=None, med_information=med_information, official=True, added_by=None)
        meds_in_db.append(med)
    model.db.session.add_all(meds_in_db)
    model.db.session.commit()

def create_accessories():
    #create 10 accessories and store them in a list
    accessories_in_db = []
    for n in range(10):
        accessory_name=f"accessory{n}"
        accessory_cost=randint(1, 10)
        accessory_description=f"a gorgeous {n} accessory"
        accessory_img = "static/img/bird1.png"
        accessory_alt = "A visual description of this swanky accessory"
        accessory=model.Accessory.create(accessory_name, accessory_cost, 
        accessory_description, accessory_img, accessory_alt)
        accessories_in_db.append(accessory)

    model.db.session.add_all(accessories_in_db)
    model.db.session.commit()

def create_users():
    #create 10 users
    for n in range(10):
        email = f"user{n}@test.com"
        password = f"test{n}"
        fname = f"User{n}"
        lname = f"{n}user"
        points = 40

        user=model.User.create(email, password, fname, lname, points)
        model.db.session.add(user)
        model.db.session.commit()
    

create_buddies()
create_accessories()
create_users()
create_meds()