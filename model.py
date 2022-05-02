#write sqlalchemy classes into, communicate w/ db in py (translates sql to py)

"""Models for medication tracker app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String,
                        unique=True,
                        nullable=False)
    password = db.Column(db.String,
                        nullable=False)
    fname = db.Column(db.String,
                        nullable=False)
    lname = db.Column(db.String)
    points = db.Column(db.Integer)
    meds = db.relationship("Med", secondary="user_meds", backref="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Med(db.Model):
    """A medication."""

    __tablename__ = 'meds'

    med_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    generic_name = db.Column(db.String,
                        nullable=False)
    brand_name = db.Column(db.String)
    med_information = db.Column(db.String)
    users = db.relationship("User", secondary="user_meds", backref="med")
    
    def __repr__(self):
        return f'<Med med_id={self.med_id}\
        generic_name={self.generic_name} brand_name ={self.brand_name}>'

class UserMeds(db.Model):
    """A user's medications."""

    __tablename__ = 'user_meds'

    usermed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    med_id = db.Column(db.Integer,
                        db.ForeignKey("med.med_id"),
                        nullable=False)

    def __repr__(self):
        return f'<UserMeds usermed_id={self.usermed_id} user_id={self.user_id} med_id={self.med_id}>'


# class Accessory(db.Model):
#     """An accessory available for purchase with points."""

#     __tablename__ = 'accessories'

#     item_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     item_name = db.Column(db.String,
#                         nullable=False)
#     item_cost = db.Column(db.Integer,
#                         nullable=False)
#     item_description = db.Column(db.Text)
#     item_img = db.Column(db.String,
#                         nullable=False)

#     def __repr__(self):
#         return f'<Accessory item_id={self.item_id} item_name={self.item_name}>'


# class Buddy(db.Model):
#     """A buddy/character that a user can have."""

#     __tablename__ = 'buddies'

#     buddy_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     buddy_name = db.Column(db.String,
#                         nullable=False)
#     buddy_description = db.Column(db.Text)
#     buddy_img = db.Column(db.String,
#                         nullable=False)
#     user_id = db.Column(db.Integer,
#                         nullable=False,

#                         #foreign key to users
#     )
#     def __repr__(self):
#         return f'<Buddy buddy_id={self.buddy_id} buddy_name={self.buddy_name}>'


# class UserInventory(db.Model):
#     """A user's inventory."""

#     # book-genres equivalent check notes for 

#     __tablename__ = 'user_inventory'

#     user_id = db.Column(db.Integer,
#                         nullable = False,
#                         #foreign key 
#     )
#     item_id = db.Column(db.Integer,
#                         nullable=False,
#                         #foreign key
#     )
#     buddy_id = db.Column(db.Integer,
#                         #foreign key
#                         )
#     def __repr__(self):
#         return f'<UserInventory user_id={self.user_id} item_id={self.item_id}>'

# class WearableBy(db.Model):
#     """Which buddies can wear which items."""

#     __tablename__ = 'wearable_by'

#     user_id = db.Column(db.Integer,
#                         nullable = False,
#                         #foreign key 
#     )
#     buddy_id = db.Column(db.Integer,
#                         nullable=False,
#                         #foreign key
#     )
#     def __repr__(self):
#         return f'<WearableBy user_id={self.user_id} buddy_id={self.buddy_id}>'

# class MedSchedule(db.Model):
#     """Medication."""

#     __tablename__ = 'wearable_by'

#     user_id = db.Column(db.Integer,
#                         nullable = False,
#                         #foreign key 
#     )
#     buddy_id = db.Column(db.Integer,
#                         nullable=False,
#                         #foreign key
#     )
#     def __repr__(self):
#         return f'<WearableBy user_id={self.user_id} buddy_id={self.buddy_id}>'


def connect_to_db(flask_app, db_uri="postgresql:///medtracker", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the medtracker db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

