from datetime import date, time, datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy(session_options={
    'expire_on_commit': False
})



class Admin(db.Model):
    """ Administrative account """

    __tablename__ = 'admins'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String,
        nullable=False,
    )

    last_name = db.Column(
        db.String,
        nullable=False,
    )

    phone = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String,
        nullable=False
    )

    access = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    def __repr__(self):
        return f"< Admin #{self.id}: {self.first_name} {self.last_name}>"
    
    @classmethod
    def create(cls, first,last,phone,username,password,access=1):
        """ create new admin """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        admin = Admin(
            first_name = first.lower(),
            last_name = last.lower(),
            phone = phone,
            username = username.lower(),
            password = hashed_pwd,
            access = access
        )

        db.session.add(admin)
        return admin
    
    @classmethod
    def authenticate(cls,username,password):
        """ find admin with 'username' and 'password'"""

        admin = cls.query.filter_by(username=username).first()

        if admin:
            is_auth = bcrypt.check_password_hash(admin.password,password)
            if is_auth:
                return admin
            
        return False
    

class Driver(db.Model):
    """ driver in system """

    __tablename__ = 'drivers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String,
        nullable=False
    )

    last_name = db.Column(
        db.String,
        nullable=False
    )

    phone = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String,
        nullable=False,
    )

    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id'),
        unique=True
    )    


    route = db.relationship('Route')

    def __repr__(self):
        return f"<Driver #{self.id}: {self.username}>"
    
    @classmethod
    def create(cls,first,last,phone,username,password,route_id=None):
        """ create new driver """

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        driver = Driver(
            first_name = first.lower(),
            last_name = last.lower(),
            phone = phone,
            username = username.lower(),
            password = hashed_password,
            route_id = route_id
        )

        db.session.add(driver)
        return driver
    
    @classmethod
    def authenticate(cls,username,password):
        """find driver with 'username' and 'password'"""

        driver =cls.query.filter_by(username=username).first()

        if driver:
            is_auth = bcrypt.check_password_hash(driver.password,password)
            if is_auth:
                return driver
            
        return False
    
class Customer(db.Model):
    """ customer in system """

    __tablename__ = 'customers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    first_name = db.Column(
        db.String,
        nullable=False,
    )

    last_name = db.Column(
        db.String,
        nullable=False,
    )

    address = db.Column(
        db.String,
        nullable=False,
    )

    phone = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    doorman = db.Column(
        db.Boolean,
        default=False
    )

    stops = db.relationship('Stop')

    def __repr__(self):
        return f"<Customer #{self.id}: {self.first_name} {self.last_name}>"
    
    @classmethod
    def create(cls,first,last,address,phone,email,doorman=False):
        """ create 'Customer' """

        customer = Customer(
            first_name = first.lower(),
            last_name = last.lower(),
            address = address.lower(),
            phone = phone,
            email = email.lower(),
            doorman = doorman
        )

        db.session.add(customer)
        return customer
    
class Stop(db.Model):
    """ stop in system """

    __tablename__ = 'stops'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customers.id'),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    status = db.Column(
        db.String,
        nullable=False,
        default='incomplete'
    )

    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id')
    )

    route = db.relationship('Route')

    customer = db.relationship('Customer')

class Route(db.Model):
    """ Routes in system """

    __tablename__ = 'routes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    date = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )

    # driver_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('drivers.id'),
    #     unique=True
    # )

    driver = db.relationship('Driver')

    stops = db.relationship('Stop')


def connect_db(app):
    db.app = app
    db.init_app(app)    
