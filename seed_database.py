import os
import json
from random import choice, randint, random, randrange
from datetime import datetime
from venv import create

from pyparsing import dict_of
import model
import server
import buddies
import accessories

os.system("dropdb medtracker")
os.system("createdb medtracker")

model.connect_to_db(server.app)
model.db.create_all()

def create_buddies():
#create buddies and store them in a list
    buddies_in_db = []
    buddy_dicts = buddies.buddy_dict
    for buddy_dict in buddy_dicts:
        buddy_name = (buddy_dicts[buddy_dict]["buddy_name"])
        buddy_description = (buddy_dicts[buddy_dict]["buddy_description"])
        buddy_img = (buddy_dicts[buddy_dict]["buddy_img1"])
        buddy_alt = (buddy_dicts[buddy_dict]["buddy_alt1"])
        buddy_img2 = (buddy_dicts[buddy_dict]["buddy_img2"])
        buddy_alt2 = (buddy_dicts[buddy_dict]["buddy_alt2"])
        buddy_img3 = (buddy_dicts[buddy_dict]["buddy_img3"])
        buddy_alt3 = (buddy_dicts[buddy_dict]["buddy_alt3"])
        buddy_img2_3 = (buddy_dicts[buddy_dict]["buddy_img2_3"])
        buddy_alt2_3 = (buddy_dicts[buddy_dict]["buddy_alt2_3"])

        buddy=model.Buddy.create(buddy_name = buddy_name,
         buddy_description=buddy_description, 
         buddy_img=buddy_img, buddy_alt=buddy_alt,
         buddy_img2=buddy_img2, buddy_alt2=buddy_alt2,
         buddy_img3=buddy_img3, buddy_alt3=buddy_alt3,
         buddy_img2_3=buddy_img2_3, buddy_alt2_3=buddy_alt2_3)
        buddies_in_db.append(buddy)
    model.db.session.add_all(buddies_in_db)
    model.db.session.commit()

def create_meds():
    meds_in_db = []
    file = open('static/data/meds.json', 'r')
    json_data = json.load(file)
    dict_of_dicts = json.loads(json_data)
    for dict in dict_of_dicts:
        med_name = (dict_of_dicts[dict]["name"])
        med_information = (dict_of_dicts[dict]["info"])
        med=model.Med.create(med_name=med_name, med_information=med_information, official=True, added_by=None)
        meds_in_db.append(med)
    model.db.session.add_all(meds_in_db)
    model.db.session.commit()

def create_accessories():
    #create accessories and store them in a list
    accessories_in_db = []
    accessory_dict = accessories.accessory_dict
    for accessory in accessory_dict:
        accessory_name=(accessory_dict[accessory]["accessory_name"])
        accessory_cost=(accessory_dict[accessory]["accessory_cost"])
        accessory_description=(accessory_dict[accessory]["accessory_description"])
        accessory_img=(accessory_dict[accessory]["accessory_img"])
        accessory_alt=(accessory_dict[accessory]["accessory_alt"])
        is_hat=(accessory_dict[accessory]["is_hat"])
        is_glasses=(accessory_dict[accessory]["is_glasses"])
        is_random=(accessory_dict[accessory]["is_random"])
        is_background=(accessory_dict[accessory]["is_background"])

        accessory=model.Accessory.create(accessory_name=accessory_name, accessory_cost=accessory_cost, 
        accessory_description=accessory_description, accessory_img=accessory_img, accessory_alt=accessory_alt,
        is_hat=is_hat, is_glasses=is_glasses, is_random=is_random, is_background=is_background)
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