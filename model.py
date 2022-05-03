"""Models for medication tracker app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    #meds is a list of Med objects
    #accessories is a list of Accessory objects
    #buddies is a list of Buddy objects
    #doses is a list of Dose objects

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
    users = db.relationship("User", secondary="user_meds", backref="meds")
    
    #doses is a list of Dose objects

    def __repr__(self):
        return f'<Med med_id={self.med_id}\
        generic_name={self.generic_name} brand_name ={self.brand_name}>'

class UserMed(db.Model):
    """A user's medications."""

    __tablename__ = 'user_meds'

    usermed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    med_id = db.Column(db.Integer,
                        db.ForeignKey("meds.med_id"),
                        nullable=False)

    def __repr__(self):
        return f'<UserMed usermed_id={self.usermed_id} user_id={self.user_id} med_id={self.med_id}>'


class Accessory(db.Model):
    """An accessory available for purchase with points."""

    __tablename__ = 'accessories'

    accessory_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    accessory_name = db.Column(db.String,
                        nullable=False)
    accessory_cost = db.Column(db.Integer,
                        nullable=False)
    accessory_description = db.Column(db.Text)
    accessory_img = db.Column(db.String,
                        nullable=False)
    users = db.relationship("User", secondary="user_inventory", backref="accessories")
    #compatible_buddies is a list of Buddy objects

    def __repr__(self):
        return f'<Accessory accessory_id={self.accessory_id} accessory_name={self.accessory_name}>'

class UserInventory(db.Model):
    """A user's inventory of accessories."""

    __tablename__ = 'user_inventory'

    userinventory_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    accessory_id = db.Column(db.Integer,
                        db.ForeignKey("accessories.accessory_id"))

    def __repr__(self):
        return f'<UserInventory userinventory_id={self.userinventory_id}\
             user_id={self.user_id} accessory_id={self.accessory_id}\
                  buddy_id={self.buddy_id}>'


class Buddy(db.Model):
    """A buddy that a user can have."""

    __tablename__ = 'buddies'

    buddy_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    buddy_name = db.Column(db.String,
                        nullable=False)
    buddy_description = db.Column(db.Text)
    buddy_img = db.Column(db.String,
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    users = db.relationship("User", secondary="user_buddies", backref="buddies")
    wearable_accessories = db.relationship("Accessory", secondary="wearable_by", backref="compatible_buddies")


class UserBuddy(db.Model):
    """A user's buddies."""

    __tablename__ = 'user_buddies'

    userbuddy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    buddy_id = db.Column(db.Integer,
                        db.ForeignKey("buddies.buddy_id"))

    def __repr__(self):
        return f'<UserBuddy userbuddy_id={self.userbuddy_id} user_id={self.user_id}\
            buddy_id={self.buddy_id}>'

class WearableBy(db.Model):
    """Which buddies can wear which accessories."""

    __tablename__ = 'wearable_by'

    wearableby_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    accessory_id = db.Column(db.Integer,
                        db.ForeignKey("accessories.accessory_id"))

    buddy_id = db.Column(db.Integer,
                        db.ForeignKey("buddies.buddy_id"))

    def __repr__(self):
        return f'<WearableBy wearableby_id={self.wearableby_id}\
            accessory_id={self.accessory_id} buddy_id={self.buddy_id}>'

class Dose(db.Model):
    """A schedule of a user's medication doses."""

    __tablename__ = 'doses'

    dose_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)

    med_id = db.Column(db.Integer,
                        db.ForeignKey("meds.med_id"),
                        nullable=False)

    date_time = db.Column(db.DateTime)
   
    taken = db.Column(db.Boolean,
                        default=False)
    user = db.relationship('User', backref='doses')
    med = db.relationship('Med', backref='doses')

    def __repr__(self):
        return f'<Dose dose_id={self.dose_id} user_id={self.user_id}\
            med_id={self.med_id} date_time={self.date_time} taken={self.taken}>'


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