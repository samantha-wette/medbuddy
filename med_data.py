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