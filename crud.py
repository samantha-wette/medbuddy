from model import db, User, Med, UserMed, Dose, UserBuddy, Buddy, UserAccessory,\
    connect_to_db
from server import app

def add_med_to_user(user_id, med_id):
    user_id = int(user_id)
    med_id = int(med_id)
    usermed = UserMed(user_id = user_id, med_id = med_id)
    db.session.add(usermed)
    db.session.commit()

def delete_med_from_user(user_id, med_id):

    user_id = int(user_id)
    print(f"USER_ID IS {user_id} OOOOOOOOO")

    med_id = int(med_id)
    print(f"MED_ID IS {med_id} OOOOOOOOO")

    usermed = UserMed(user_id = user_id, med_id = med_id)
    print(f"USERMED IS {usermed} OOOOOOOOO")
    db.session.delete(usermed)
    db.session.commit()

# def add_dose_to_user(user_id, dose_id):
#     user_id = int(user_id)
#     dose_id = int(dose_id)

            #added_dose = crud.add_dose_to_user(user_id = user_id, dose_id = dose_id)    

# add to UserMed table the userID and medID and medNAME
# add an entry to the dose table
    # usermed_table = UserMed.__tablename__
    
    # result = db.session.query(UserMed).join(Med).filter(UserMed.user_id == Med.users).one()
    # print(result)


    # result = User.query.join(usermed_table).join(Med)\
    #     .filter(UserMed.user_id == User.user_id) &\
    #         (UserMed.med_id == Med.med_id).all()
        
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
