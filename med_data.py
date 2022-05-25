import os
import json
from random import choice, randint, random, randrange
from datetime import datetime
import model
import server

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static", "data", "meds.json")
json_data = json.loads(open(json_url).read())
med_data = json_data["results"]
# for med in med_data:
#     print(med["med_name"])
#     print(med["med_name"])
#     print("**")    

# for n in range(10):
#     med_name=
#     med_name=
#     med_information=
#     med=model.Med.create(med_name, med_name, med_information, official=True, added_by=None)
# model.db.session.add_all(meds_in_db
# model.db.session.commit()
