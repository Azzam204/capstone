
from flask_wtf import FlaskForm
from datetime import time
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, TimeField, DateField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Email, Length, ValidationError, Optional, NumberRange
from models import *

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username',
                           validators=[InputRequired(message='Username required')])
    password = PasswordField('Password',
                             validators=[InputRequired(message='Input password')])

class RouteForm(FlaskForm):
    """route form"""

    name = StringField('Area',
                       validators=[InputRequired(message="Name required")])
    
class DriverForm(FlaskForm):
    """Driver form"""

    first_name = StringField('First Name',
                             validators=[InputRequired(message='First name required')])
    
    last_name = StringField('Last Name',
                             validators=[InputRequired(message='Last name required')])
    
    phone = IntegerField('Phone',
                        validators=[InputRequired(message='Phone number required'),NumberRange(min=1000000000)])
    
    username = StringField('Username',
                           validators=[InputRequired(message='Username required'),Length(min=3)])
    
    password = PasswordField('Password',
                           validators=[InputRequired(message='Password required')])
    
class StopForm(FlaskForm):
    """Stop form"""
    
    start_time = TimeField('Start time',
                           validators= [InputRequired(message='Start time required')])
    
    end_time = TimeField('End time',
                           validators= [InputRequired(message='End time required')])
    
    route_id = SelectField('Route',
                           validators=[Optional()])
    
    def validate_end_time(form, field):
        if field.data < form.start_time.data:
            raise ValidationError("End time must be later than start time")

    def __init__(self):
        super(StopForm, self).__init__()
        self.route_id.choices =[('0','')]+[(r.id, r.name) for r in Route.query.all()]
        self.start_time.data = time(18)
        self.end_time.data = time(21)



class AdminForm(FlaskForm):
    """Admin Form"""

    first_name = StringField('First Name',
                             validators=[InputRequired(message='First name required')])
    
    last_name = StringField('Last Name',
                             validators=[InputRequired(message='Last name required')])
    
    phone = IntegerField('Phone',
                        validators=[InputRequired(message='Phone number required'),NumberRange(min=1000000000)])
    
    username = StringField('Username',
                           validators=[InputRequired(message='Username required'),Length(min=3)])
    
    password = PasswordField('Password',
                           validators=[InputRequired(message='Password required')])
    


class CustomerForm(FlaskForm):
    """Customer Form"""

    first_name = StringField('First Name',
                            validators=[InputRequired(message='First name required')])
    
    last_name = StringField('Last Name',
                            validators=[InputRequired(message='Last name required')])
    
    address = StringField('Address',
                          validators=[InputRequired('Address required')])
    
    phone = IntegerField('Phone',
                        validators=[InputRequired(message='Phone number required'),NumberRange(min=1000000000)])
    
    email = StringField('E-mail',
                        validators=[InputRequired(message='Email required'),Email(message='Invalid email')])
    
    doorman = BooleanField('Doorman')


class RouteDriverDropdown(FlaskForm):
    """Select form to assigne drivers to routes"""

    driver_id = SelectField()

    def __init__(self):
        super(RouteDriverDropdown, self).__init__()
        self.driver_id.choices = [(d.id, d.username) for d in Driver.query.all()]

