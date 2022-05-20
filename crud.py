from model import db, User, Med, UserMed, Dose, UserBuddy, Buddy, UserAccessory,\
    connect_to_db
from server import app

def delete_doses_of_med_from_user(user_id, med_id):
    user_id = int(user_id)
    med_id = int(med_id)
    doses = Dose.get_upcoming_by_user_and_med(user_id=user_id, med_id=med_id)
    for dose in doses:
        db.session.delete(dose)
    db.session.commit()

def delete_med_from_user(user_id, med_id):
    user_id = int(user_id)
    med_id = int(med_id)
    usermed = UserMed.query.filter(UserMed.user_id==user_id, UserMed.med_id == med_id).first()        
    db.session.delete(usermed)
    db.session.commit()
        
def add_buddy_to_user(user_id, buddy_id):
    user_id = int(user_id)
    buddy_id = int(buddy_id)
    userbuddy = UserBuddy(user_id = user_id, buddy_id = buddy_id)
    db.session.add(userbuddy)
    db.session.commit()

    #added-by

    
def add_accessory_to_user(user_id, accessory_id):
    user_id = int(user_id)
    accessory_id = int(accessory_id)
    useraccessory = UserAccessory(user_id = user_id, accessory_id = accessory_id)
    db.session.add(useraccessory)
    db.session.commit()



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
