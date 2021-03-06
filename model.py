"""Models for medication tracker app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy import CheckConstraint

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
    points = db.Column(db.Integer, nullable=False)
    __table_args__ = (CheckConstraint (points >= 0, name ='check_points_zero_or_above'), {})

    #usermeds is a list of UserMed objects
    #meds is a list of Med objects
    #accessories is a list of Accessory objects
    #buddies is a list of Buddy objects
    #doses is a list of Dose objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} password={self.password}>'
 
    @classmethod
    def create(cls, email, password, fname, lname, points=15):
        """create and return a new user"""
        return cls(email=email,
                password=password,
                fname=fname,
                lname=lname,
                points=points)
    
    @classmethod
    def earn_points(cls, user_id, num):
        """Add to a user's point total"""
        user = cls.query.get(user_id)
        new_points = User.points + num
        user.points = new_points

    @classmethod
    def spend_points(cls, user_id, num):
        """Add to a user's point total"""
        print("in the function")
        user = cls.query.get(user_id)
        new_points = user.points - num
        user.points = new_points

    @classmethod
    def get_by_id(cls, user_id):
        '""Find a user by their ID"""'
        return User.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        """Find a user by email"""
        return cls.query.filter(User.email == email).first()        

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
        return user.doses
        
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
    med_name = db.Column(db.String,
                        nullable=False)
    med_information = db.Column(db.String)
    official = db.Column(db.Boolean, nullable=False)
    added_by = db.Column(db.Integer)
    
    #doses is a list of Dose objects
    #usermeds is a list of UserMed objects

    def __repr__(self):
        return f'<Med med_id={self.med_id}\
        med_name={self.med_name}>'

    @classmethod
    def create(cls, med_name, med_information, official, added_by=None):
        """Create and return a Med object"""
        return cls(med_name=med_name,
                med_information=med_information,
                official=official,
                added_by = added_by)

    @classmethod
    def get_by_id(cls, med_id):
        """Find a med by its id"""
        return cls.query.filter(cls.med_id == med_id).first()

    @classmethod
    def get_by_med_name(cls, med_name):
        """Find a med by its name"""
        return cls.query.filter(Med.med_name == med_name).first()

    @classmethod
    def get_doses(cls, med_id):
        """Get scheduled doses for a certain med"""
        med = cls.query.options(db.joinedload('doses')).get(med_id)
        return med.doses

    @classmethod
    def get_official(cls):
        """Find a user's buddies"""
        return cls.query.filter(Med.official == True).all()

    @classmethod
    def all_meds(cls):
        return cls.query.all()

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
    taken_regularly = db.Column(db.Boolean,
                        default=False)
    taken_as_needed = db.Column(db.Boolean,
                        default=False)
    currently_taking = db.Column(db.Boolean, default=True)
    typical_dose = db.Column(db.String, default=None)
    last_updated_date = db.Column(db.Date, default=None)
    last_updated_time = db.Column(db.Time, default=None)
    med = db.relationship("Med", backref="usermeds")
    user = db.relationship("User", backref="usermeds")

    #doses is a list of Dose objects

    def __repr__(self):
        return f'<UserMed usermed_id={self.usermed_id} user_id={self.user_id} med_id={self.med_id} taken_regularly={self.taken_regularly}>'
    
    @classmethod
    def create(cls,
                user_id,
                med_id,
                taken_regularly,
                taken_as_needed,
                currently_taking,
                typical_dose=None,
                last_updated_date=None,
                last_updated_time=None):
        """Create and return a UserMed object"""
        return cls(user_id=user_id,
                med_id=med_id,
                taken_regularly=taken_regularly,
                taken_as_needed=taken_as_needed,
                currently_taking=currently_taking,
                typical_dose=typical_dose,
                last_updated_date=last_updated_date,
                last_updated_time=last_updated_time)
    
    @classmethod
    def update_last_updated(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        usermed.last_updated_date = date.today()
        usermed.last_updated_time = datetime.now().time()


    @classmethod
    def make_taken_regularly(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        if usermed.taken_regularly == False:
            usermed.taken_regularly = True

    @classmethod
    def make_not_taken_regularly(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        print(f"THE UESRMED IS {usermed}")
        if usermed.taken_regularly ==True:
            usermed.taken_regularly=False
        print(f"UPDATED USERMED IS {usermed}")

    @classmethod
    def set_taken_as_needed(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        if usermed.taken_as_needed == False:
            usermed.taken_as_needed = True

    @classmethod
    def set_not_taken_as_needed(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        if usermed.taken_as_needed ==True:
            usermed.taken_as_needed=False

    @classmethod
    def set_currently_taking(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        if usermed.currently_taking == False:
            usermed.currently_taking = True

    @classmethod
    def set_not_currently_taking(cls, usermed_id):
        usermed = cls.query.get(usermed_id)
        if usermed.currently_taking ==True:
            usermed.currently_taking=False

    @classmethod
    def set_typical_dose(cls, usermed_id, typical_dose):
        usermed = cls.query.get(usermed_id)
        usermed.typical_dose = typical_dose


    @classmethod
    def as_needed_by_user(cls, user_id):
        return cls.query.filter(cls.taken_as_needed == True, cls.user_id == user_id).all()

    @classmethod
    def get_by_user_and_med(cls, user_id, med_id):
        return cls.query.filter(cls.user_id == user_id, cls.med_id == med_id,).first()


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
    accessory_alt = db.Column(db.String)
    is_hat = db.Column(db.Boolean, default=False)
    is_glasses = db.Column(db.Boolean, default=False)
    is_random = db.Column(db.Boolean, default=False)
    is_background = db.Column(db.Boolean, default=False)
    users = db.relationship("User", secondary="user_accessory", backref="accessories")
    #compatible_buddies is a list of Buddy objects

    def __repr__(self):
        return f'<Accessory accessory_id={self.accessory_id} accessory_name={self.accessory_name}>'
    
    @classmethod
    def create(cls, accessory_name, accessory_cost, accessory_description, accessory_img, accessory_alt, is_hat, is_glasses, is_random, is_background):
        """Create and return an Accessory object"""
        return cls(accessory_name=accessory_name,
                accessory_cost=accessory_cost,
                accessory_description=accessory_description,
                accessory_img=accessory_img,
                accessory_alt=accessory_alt,
                is_hat=is_hat,
                is_glasses=is_glasses,
                is_random=is_random,
                is_background=is_background
                )

    @classmethod
    def get_by_id(cls, accessory_id):
        """Find an accessory by its id"""
        return cls.query.filter(cls.accessory_id == accessory_id).first()

    @classmethod
    def get_by_cost(cls, max_price):
        """Find a list of accessories by maximum price"""
        return cls.query.filter(cls.accessory_cost <= max_price).all()

    @classmethod
    def all_accessories(cls):
        return cls.query.all()


class UserAccessory(db.Model):
    """A user's inventory of accessories. (secondary table)"""

    __tablename__ = 'user_accessory'

    useraccessory_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    accessory_id = db.Column(db.Integer,
                        db.ForeignKey("accessories.accessory_id"))

    def __repr__(self):
        return f'<UserAccessory useraccessory_id={self.useraccessory_id}\
             user_id={self.user_id} accessory_id={self.accessory_id}'

class Buddy(db.Model):
    """A buddy that a user can have."""

    __tablename__ = 'buddies'

    buddy_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    buddy_name = db.Column(db.String,
                        nullable=False)
    buddy_description = db.Column(db.Text)

    img_O_O = db.Column(db.String)
    alt_O_O = db.Column(db.String)
    img_O_a = db.Column(db.String)
    alt_O_a = db.Column(db.String)
    img_O_b = db.Column(db.String)
    alt_O_b = db.Column(db.String)
    img_O_c = db.Column(db.String)
    alt_O_c = db.Column(db.String)
    img_a_O = db.Column(db.String)
    alt_a_O = db.Column(db.String)
    img_a_a = db.Column(db.String)
    alt_a_a = db.Column(db.String)
    img_a_b = db.Column(db.String)
    alt_a_b = db.Column(db.String)
    img_a_c = db.Column(db.String)
    alt_a_c = db.Column(db.String)
    img_b_O = db.Column(db.String)
    alt_b_O = db.Column(db.String)
    img_b_a = db.Column(db.String)
    alt_b_a = db.Column(db.String)
    img_b_b = db.Column(db.String)
    alt_b_b = db.Column(db.String)
    img_b_c = db.Column(db.String)
    alt_b_c = db.Column(db.String)
    img_c_O = db.Column(db.String)
    alt_c_O = db.Column(db.String)
    img_c_a = db.Column(db.String)
    alt_c_a = db.Column(db.String)
    img_c_b = db.Column(db.String)
    alt_c_b = db.Column(db.String)
    img_c_c = db.Column(db.String)
    alt_c_c = db.Column(db.String)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    users = db.relationship("User", secondary="user_buddies", backref="buddies")

    @classmethod
    def create(cls, buddy_name, buddy_description,
    img_O_O, alt_O_O,
    img_O_a, alt_O_a,
    img_O_b, alt_O_b,
    img_O_c, alt_O_c,
    img_a_O, alt_a_O,
    img_a_a, alt_a_a,
    img_a_b, alt_a_b,
    img_a_c, alt_a_c,
    img_b_O, alt_b_O,
    img_b_a, alt_b_a,
    img_b_b, alt_b_b,
    img_b_c, alt_b_c,
    img_c_O, alt_c_O,
    img_c_a, alt_c_a,
    img_c_b, alt_c_b,
    img_c_c, alt_c_c


    ):
        """Create and return a Buddy object"""
        return cls(buddy_name=buddy_name,
                buddy_description=buddy_description,


                img_O_O = img_O_O,
                alt_O_O = alt_O_O,
                img_O_a = img_O_a,
                alt_O_a = alt_O_a,
                img_O_b = img_O_b,
                alt_O_b = alt_O_b,
                img_O_c = img_O_c,
                alt_O_c = alt_O_c,
                img_a_O = img_a_O,
                alt_a_O = alt_a_O,
                img_a_a = img_a_a,
                alt_a_a = alt_a_a,
                img_a_b = img_a_b,
                alt_a_b = alt_a_b,
                img_a_c = img_a_c,
                alt_a_c = alt_a_c,
                img_b_O = img_b_O,
                alt_b_O = alt_b_O,
                img_b_a = img_b_a,
                alt_b_a = alt_b_a,
                img_b_b = img_b_b,
                alt_b_b = alt_b_b,
                img_b_c = img_b_c,
                alt_b_c = alt_b_c,
                img_c_O = img_c_O,
                alt_c_O = alt_c_O,
                img_c_a = img_c_a,
                alt_c_a = alt_c_a,
                img_c_b = img_c_b,
                alt_c_b = alt_c_b,
                img_c_c = img_c_c,
                alt_c_c = alt_c_c
                )

    @classmethod
    def get_by_id(cls, buddy_id):
        """Find a buddy by its id"""
        return cls.query.filter(cls.buddy_id == buddy_id).first()

    @classmethod
    def get_by_user(cls, user_id):
        """Find a user's buddies"""
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def all_buddies(cls):
        return cls.query.all()


class UserBuddy(db.Model):
    """A user's buddies."""

    __tablename__ = 'user_buddies'

    userbuddy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable = False)
    buddy_id = db.Column(db.Integer,
                        db.ForeignKey("buddies.buddy_id"),
                        nullable = False)
    
    primary_buddy = db.Column(db.Boolean, default=False)

    url = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, nullable=False)

    buddy = db.relationship("Buddy", backref="userbuddies")
    user = db.relationship("User", backref="userbuddies")

    def __repr__(self):
        return f'<UserBuddy userbuddy_id={self.userbuddy_id} user_id={self.user_id}\
            buddy_id={self.buddy_id} primary={self.primary_buddy}>'
    
    @classmethod
    def create(cls, user_id, buddy_id, url, alt, primary_buddy=False):
        """Create and return a UserBuddy object"""
        return cls(user_id=user_id,
                buddy_id=buddy_id,
                primary_buddy=primary_buddy,
                url=url,
                alt=alt)

    @classmethod
    def get_buddy_by_userbuddy(cls, userbuddy_id):
        """Get a buddy's ID based on the userbuddy ID"""
        print(f"IN THE CLASS METHOD, userbuddy_id is {userbuddy_id}")
        userbuddy = cls.query.get(userbuddy_id)
        print(f"we found {userbuddy} as the userbuddy")
        return userbuddy

    @classmethod
    def make_primary_buddy(cls, userbuddy_id):
        """Mark a buddy as a user's primary buddy"""
        userbuddy = cls.query.get(userbuddy_id)
        userbuddy.primary_buddy = True
    
    @classmethod
    def update_url(cls, userbuddy_id, buddy_url, buddy_alt):
        """Mark a buddy as a user's primary buddy"""
        userbuddy = cls.query.get(userbuddy_id)
        userbuddy.url = buddy_url
        userbuddy.alt = buddy_alt

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

    usermed_id = db.Column(db.Integer,
                        db.ForeignKey("user_meds.usermed_id"),
                        nullable=False)

    date = db.Column(db.Date, default=None)

    time = db.Column(db.Time, default=None)

    taken = db.Column(db.Boolean,
                        default=False)

    time_taken = db.Column(db.DateTime)

    notes = db.Column(db.Text, default=None)

    amount=db.Column(db.String, default=None)

    cancelled = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='doses')
    med = db.relationship('Med', backref='doses')
    usermed = db.relationship('UserMed', backref='doses')

    def __repr__(self):
        return f'<Dose dose_id={self.dose_id} user_id={self.user_id}\
            med_id={self.med_id}>'

    @classmethod
    def create(cls, user_id, med_id, usermed_id, date=date, time=time, time_taken=None, taken=False, notes=None, amount=amount, cancelled=False):
        """Create and return a Dose object"""
        return cls(user_id=user_id,
                med_id=med_id,
                usermed_id=usermed_id,
                date=date,
                time=time,
                time_taken=time_taken,
                taken = taken,
                notes=notes,
                amount=amount,
                cancelled=cancelled)

    @classmethod
    def get_upcoming_by_user_and_med(cls, user_id, med_id):
        today = date.today()
        return cls.query.filter(Dose.user_id == user_id, Dose.med_id == med_id, Dose.date >= today,
        Dose.taken == False).all()

    @classmethod
    def cancel_upcoming_doses_by_usermed(cls, usermed_id):
        doses = cls.query.filter(Dose.usermed_id == usermed_id, Dose.taken == False).all()
        for dose in doses:
            del(dose)

    @classmethod
    def get_by_user(cls, user_id):
        """Get all doses from a user"""
        return cls.query.filter(Dose.user_id == user_id).all()

    @classmethod
    def get_taken_by_user(cls, user_id):
        """Get all doses already taken from a user"""
        return cls.query.filter(Dose.user_id == user_id, Dose.taken == True).all()
    
    @classmethod
    def get_missed_by_user(cls, user_id):
        """Get all doses missed by a user"""
        today = date.today()
        return cls.query.filter(Dose.user_id == user_id, Dose.taken == False, Dose.date < today).all()

    @classmethod
    def get_upcoming_by_user(cls, user_id):
        """Get all today's upcoming doses by a user."""
                
        today = date.today()

        return cls.query.filter(Dose.user_id == user_id, Dose.taken == False,
        Dose.date == today).all()

    @classmethod
    def mark_taken(cls, dose_id, time_taken, notes=None, amount=None):
        """Mark a dose as taken"""
        dose = cls.query.get(dose_id)
        dose.taken = True
        dose.time_taken = time_taken
        dose.notes = notes
        dose.amount = amount

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