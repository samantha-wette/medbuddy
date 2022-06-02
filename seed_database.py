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
        print(buddy_dict)
        print(buddy_dicts[buddy_dict])
        print(buddy_dicts[buddy_dict]['buddy_name'])
        print("****OK****")
        buddy_name = (buddy_dicts[buddy_dict]["buddy_name"])
        buddy_description = (buddy_dicts[buddy_dict]["buddy_description"])
        img_O_O = (buddy_dicts[buddy_dict]["O_O"])
        alt_O_O = (buddy_dicts[buddy_dict]["alt_O_O"])
        img_O_a = (buddy_dicts[buddy_dict]["O_a"])
        alt_O_a = (buddy_dicts[buddy_dict]["alt_O_a"])
        img_O_b = (buddy_dicts[buddy_dict]["O_b"])
        alt_O_b = (buddy_dicts[buddy_dict]["alt_O_b"])
        img_O_c = (buddy_dicts[buddy_dict]["O_c"])
        alt_O_c = (buddy_dicts[buddy_dict]["alt_O_c"])
        img_a_O = (buddy_dicts[buddy_dict]["a_O"])
        alt_a_O = (buddy_dicts[buddy_dict]["alt_a_O"])
        img_a_a = (buddy_dicts[buddy_dict]["a_a"])
        alt_a_a = (buddy_dicts[buddy_dict]["alt_a_a"])
        img_a_b = (buddy_dicts[buddy_dict]["a_b"])
        alt_a_b = (buddy_dicts[buddy_dict]["alt_a_b"])
        img_a_c = (buddy_dicts[buddy_dict]["a_c"])
        alt_a_c = (buddy_dicts[buddy_dict]["alt_a_c"])
        img_b_O = (buddy_dicts[buddy_dict]["b_O"])
        alt_b_O = (buddy_dicts[buddy_dict]["alt_b_O"])
        img_b_a = (buddy_dicts[buddy_dict]["b_a"])
        alt_b_a = (buddy_dicts[buddy_dict]["alt_b_a"])
        img_b_b = (buddy_dicts[buddy_dict]["b_b"])
        alt_b_b = (buddy_dicts[buddy_dict]["alt_b_b"])
        img_b_c = (buddy_dicts[buddy_dict]["b_c"])
        alt_b_c = (buddy_dicts[buddy_dict]["alt_b_c"])
        img_c_O = (buddy_dicts[buddy_dict]["c_O"])
        alt_c_O = (buddy_dicts[buddy_dict]["alt_c_O"])
        img_c_a = (buddy_dicts[buddy_dict]["c_a"])
        alt_c_a = (buddy_dicts[buddy_dict]["alt_c_a"])
        img_c_b = (buddy_dicts[buddy_dict]["c_b"])
        alt_c_b = (buddy_dicts[buddy_dict]["alt_c_b"])
        img_c_c = (buddy_dicts[buddy_dict]["c_c"])
        alt_c_c = (buddy_dicts[buddy_dict]["alt_c_c"])

        buddy=model.Buddy.create(
                buddy_name = buddy_name,
                buddy_description = buddy_description,
                img_O_O = img_O_O,
                alt_O_O = alt_O_O,
                img_O_a = img_O_a,
                alt_O_a = alt_O_a,
                img_O_b = img_O_b,
                alt_O_b = alt_O_b,
                img_O_c = img_O_c,
                alt_O_c = alt_O_c,
                img_a_O = img_a_O,
                alt_a_O = alt_a_O,
                img_a_a = img_a_a,
                alt_a_a = alt_a_a,
                img_a_b = img_a_b,
                alt_a_b = alt_a_b,
                img_a_c = img_a_c,
                alt_a_c = alt_a_c,
                img_b_O = img_b_O,
                alt_b_O = alt_b_O,
                img_b_a = img_b_a,
                alt_b_a = alt_b_a,
                img_b_b = img_b_b,
                alt_b_b = alt_b_b,
                img_b_c = img_b_c,
                alt_b_c = alt_b_c,
                img_c_O = img_c_O,
                alt_c_O = alt_c_O,
                img_c_a = img_c_a,
                alt_c_a = alt_c_a,
                img_c_b = img_c_b,
                alt_c_b = alt_c_b,
                img_c_c = img_c_c,
                alt_c_c = alt_c_c)

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
        points = 25

        user=model.User.create(email, password, fname, lname, points)
        model.db.session.add(user)
        model.db.session.commit()
    

create_buddies()
create_accessories()
create_users()
create_meds()