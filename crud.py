from model import db, User, Med, UserMed, Dose, connect_to_db
from server import app

def add_med_to_user(user_id, med_id):
    user_id = int(user_id)
    med_id = int(med_id)
    usermed = UserMed(user_id = user_id, med_id = med_id)

# add to UserMed table the userID and medID and medNAME
# add an entry to the dose table
    db.session.add(usermed)
    db.session.commit()
    # usermed_table = UserMed.__tablename__
    
    # result = db.session.query(UserMed).join(Med).filter(UserMed.user_id == Med.users).one()
    # print(result)


    # result = User.query.join(usermed_table).join(Med)\
    #     .filter(UserMed.user_id == User.user_id) &\
    #         (UserMed.med_id == Med.med_id).all()
        
# session.query(User.user_id, User.last_name, Role.name, Med.__tablename__).filter(
#         meds.users.c.user_id == User.id).filter(roles_users.c.role_id == Role.id).all()

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
