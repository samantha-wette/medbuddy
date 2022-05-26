from model import db, UserAccessory, connect_to_db
from server import app
    
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