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
        return f'<User user_id={self.user_id} email={self.email} password={self.password}>'
 
    @classmethod
    def create(cls, email, password, fname, lname):
        """create and return a new user"""
        return cls(email=email,
                password=password,
                fname=fname,
                lname=lname)

    @classmethod
    def get_by_id(cls, user_id):
        '""Find a user by their ID"""'
        return User.query.get(2)

    @classmethod
    def get_by_email(cls, email):
        """Find a user by email"""
        print('in the get_by_email function')
        print(cls)
        print(email)
        #return cls.query.filter(cls.email == cls.email).first()
        this_user = User.query.get(2)
        print(this_user)
        #return cls.query.filter(cls.email == email).first()
        #return cls.query.filter(email x== email).first()

    @classmethod
    def get_meds(cls, user_id):
        """Return a list of a user's meds"""
        user = cls.query.options(db.joinedload('meds')).get(user_id)
        return user.meds

    @classmethod
    def get_points(cls, user_id):
        """Return a user's point total"""
        user=cls.query.get(user_id)
        return user.points

    @classmethod
    def get_doses(cls, user_id):
        """Return a user's med scheduled doses"""
        user = cls.query.options(db.joinedload('doses')).get(user_id)
        return user.doses

    @classmethod
    def get_doses_taken(cls, user_id):
        """Return a user's taken med doses"""
        user = cls.query.options(db.joinedload('doses')).filter(cls.user_id ==
        user_id, Dose.taken == True)
        
    @classmethod
    def get_buddies(cls, user_id):
        """Return a user's buddies"""
        user = cls.query.options(db.joinedload('buddies')).get(user_id)
        return user.buddies

    @classmethod
    def get_accessories(cls, user_id):
        """Return a user's accessories"""
        user = cls.query.options(db.joinedload('accessories')).get(user_id)
        return user.accessories

    @classmethod
    def all_users(cls):
        return cls.query.all()

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

    @classmethod
    def create(cls, generic_name, brand_name, med_information):
        """Create and return a Med object"""
        return cls(generic_name=generic_name,
                brand_name=brand_name,
                med_information=med_information)

    @classmethod
    def get_by_id(cls, med_id):
        """Find a med by its id"""
        return cls.query.filter(cls.med_id == med_id).first()

    @classmethod
    def get_by_generic_name(cls, generic_name):
        """Find a med by its generic name"""
        return cls.query.filter(cls.generic_name == generic_name).first()

    @classmethod
    def get_by_brand_name(cls, brand_name):
        """Find a med by its brand name"""
        return cls.query.filter(cls.brand_name == brand_name).first()

    @classmethod
    def get_doses(cls, med_id):
        """Get scheduled doses for a certain med"""
        med = cls.query.options(db.joinedload('doses')).get(med_id)
        return med.doses

    @classmethod
    def all_meds(cls):
        return cls.query.all()
   

class UserMed(db.Model):
    """A user's medications. (secondary table)"""

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
    
    @classmethod
    def create(cls, accessory_name, accessory_cost, accessory_description, accessory_img):
        """Create and return an Accessory object"""
        return cls(accessory_name=accessory_name,
                accessory_cost=accessory_cost,
                accessory_description=accessory_description,
                accessory_img=accessory_img)

    @classmethod
    def get_by_id(cls, accessory_id):
        """Find an accessory by its id"""
        return cls.query.filter(cls.accessory_id == accessory_id).first()

    @classmethod
    def get_by_cost(cls, max_price):
        """Find a list of accessories by maximum price"""
        return cls.query.filter(cls.accessory_cost <= max_price).all()

    @classmethod
    def get_all_compatible_buddies(cls, accessory_id):
        """Return a list of all buddies who can wear an acceessory"""
        accessory = cls.query.options(db.joinedload('compatible_buddies')).get(accessory_id)
        return accessory.compatible_buddies

    @classmethod
    def all_accessories(cls):
        return cls.query.all()


class UserInventory(db.Model):
    """A user's inventory of accessories. (secondary table)"""

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

    @classmethod
    def create(cls, buddy_name, buddy_description, buddy_img):
        """Create and return a Buddy object"""
        return cls(buddy_name=buddy_name,
                buddy_description=buddy_description,
                buddy_img=buddy_img)

    @classmethod
    def get_by_id(cls, buddy_id):
        """Find a buddy by its id"""
        return cls.query.filter(cls.buddy_id == buddy_id).first()

    @classmethod
    def get_by_user(cls, user_id):
        """Find a user's buddies"""
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def get_all_wearable_accessories(cls, buddy_id):
        """Return a list of all accessories wearable by a buddy"""
        buddy = cls.query.options(db.joinedload('wearable_accessories')).get(buddy_id)
        return buddy.wearable_accessories

    @classmethod
    def all_buddies(cls):
        return cls.query.all()


class UserBuddy(db.Model):
    """A user's buddies. (secondary table)"""

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
    """Which buddies can wear which accessories. (secondary table)"""

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


    @classmethod
    def create(cls, user_id, med_id, date_time):
        """Create and return a Dose object"""
        return cls(user_id=user_id,
                med_id=med_id,
                date_time=date_time)

    @classmethod
    def mark_taken(cls, dose_id):
        """Mark a dose as taken"""
        dose = cls.query.get(dose_id)
        dose.taken = True

    @classmethod
    def all_doses(cls):
        return cls.query.all()

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