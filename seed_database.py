import os
import json
from random import choice, randint, random, randrange
from datetime import datetime

import model
import server

os.system("dropdb medtracker")
os.system("createdb medtracker")

model.connect_to_db(server.app)
model.db.create_all()

#create 5 buddies and store them in a list
buddies_in_db = []
for n in range(5):
    buddy_name = f"buddy{n}"
    buddy_description = "a cool friend called {n}"
    buddy_img = "/Users/samanthawette/med_tracker/static/img/cat1.png"

    buddy=model.Buddy.create(buddy_name, buddy_description, buddy_img)
    buddies_in_db.append(buddy)

#create 10 meds and store them in a list
meds_in_db = []
for n in range(10):
    generic_name=f"med{n}"
    brand_name=f"fancy{n}"
    med_information="https://www.fda.gov/"

    med=model.Med.create(generic_name, brand_name, med_information)
    meds_in_db.append(med)
model.db.session.add_all(meds_in_db)
model.db.session.commit()


#create 10 accessories and store them in a list
accessories_in_db = []
for n in range(10):
    accessory_name=f"accessory{n}"
    accessory_cost=randint(1, 10)
    accessory_description=f"a gorgeous {n} accessory"
    accessory_img = "/Users/samanthawette/med_tracker/static/img/bird1.png"

    accessory=model.Accessory.create(accessory_name, accessory_cost, 
    accessory_description, accessory_img)
    accessories_in_db.append(accessory)

model.db.session.add_all(accessories_in_db)
model.db.session.commit()
#create 10 users and schedule 4 med doses each
for n in range(10):
    email = f"user{n}@test.com"
    password = f"test{n}"
    fname = f"User{n}"
    lname = "{n}user"

    user=model.User.create(email, password, fname, lname)
    model.db.session.add(user)
    model.db.session.commit()
    
    for _ in range(4):
        random_med = choice(meds_in_db)
        



    for _ in range(4):
        random_med = choice(meds_in_db)
        date_time = f"(2022, {randint(1, 12)}, {randint(1, 25)})"
        dose=model.Dose.create(user.user_id, random_med.med_id, date_time)

        model.db.session.add(dose)
        model.db.session.commit()