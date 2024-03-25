import requests
from api import *
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import Null, desc

from forms import *
from models import db, connect_db, Admin, Customer, Driver, Route, Stop

CUR_USER = 'cur_user'
USER_TYPE = 'user_type'
admin_type =  "<class 'models.Admin'>"
driver_type =  "<class 'models.Driver'>"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///deliverease'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'fartnoise'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CUR_USER in session:
        
        if session[USER_TYPE] == admin_type:
            g.user = Admin.query.get(session[CUR_USER])

        elif session[USER_TYPE] == driver_type:
            g.user = Driver.query.get(session[CUR_USER])
        
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[USER_TYPE] = str(type(user))

    session[CUR_USER] = user.id


def do_logout():
    """Logout user."""

    if CUR_USER in session:
        del session[CUR_USER]
        del session[USER_TYPE]

########################################################################
# Homepage 
        
@app.route('/')
def homepage():
    """ show homepage """
    if g.user:
        if session[USER_TYPE] == driver_type:
            return redirect('/driver/dashboard')
    
        elif session[USER_TYPE] == admin_type:
            return redirect('/admin/dashboard')
    
    
    return redirect('/login')
    

@app.route('/login', methods= ['GET','POST'])
def login():
    """ Handle log in """

    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.authenticate(form.username.data.lower(),
                                   form.password.data)
        
        driver = Driver.authenticate(form.username.data.lower(),
                                     form.password.data)

        if admin:
            do_login(admin)
            flash(f'Hello, {admin.first_name.capitalize()}!', 'success')
            return redirect('/')
        
        if driver:
            do_login(driver)
            flash(f'Hello, {driver.first_name.capitalize()}!', 'success')
            return redirect('/')
        
        flash("Invalid credentials", "danger")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ Handle logout of user """
    do_logout()
    flash('Signed out successfully.', 'success')
    return redirect('/login')


@app.route('/admin/dashboard')
def show_admin_dash():
    
    if g.user:
        drivers = Driver.query.all()
        routes = Route.query.all()
        stops = Stop.query.order_by(desc(Stop.route_id)).all()
        admins = Admin.query.filter(Admin.id != g.user.id).all()
        customers = Customer.query.all()
        route_form = RouteForm()
        driver_form = DriverForm()
        stop_form = StopForm()
        admin_form = AdminForm()
        


        return render_template('admin-dash.html',
                            drivers = drivers,
                            routes = routes,
                            stops = stops,
                            admins = admins,
                            customers = customers,
                            route_form =route_form,
                            driver_form=driver_form,
                            stop_form=stop_form,
                            admin_form=admin_form)
    return redirect('/')

@app.route('/driver/dashboard')
def show_driver_dash():

    if g.user:

        route_id = g.user.route_id
        stops = Stop.query.filter_by(route_id = route_id).order_by(desc(Stop.status)).all()

        return render_template('driver-dash.html', stops=stops)

    return redirect('/')    

@app.route('/driver/opt_route')
def show_optomized_route():

    if g.user:

        route = Route.query.get(g.user.route_id)

        add_arr = [ stop.customer.address for stop in route.stops]

        data = create_data(add_arr)
        
        resp = requests.post(url,params=params,json=data)

        stops_resp = resp.json()['geocodingResults']['intermediates']

        id_list = [(route.stops[stops_resp.index(place)], place['placeId'] ) for place in stops_resp]

        opt_index = resp.json()['routes'][0]['optimizedIntermediateWaypointIndex']

        opt_route = [id_list[index] for index in opt_index]

        return render_template('opt_route.html',
                               opt_route=opt_route,
                               route=route)


    return redirect('/')



@app.route('/customers')
def find_and_create_cust():

    if g.user:
        form = CustomerForm()
        
        search = request.args.get('q')
        if not search:

            customers = Customer.query.all()

            return render_template('customers.html',
                                   customers=customers,
                                   form=form)
        
        else:

            customers = Customer.query.filter(Customer.first_name.ilike(f"%{search}%") | Customer.last_name.ilike(f"%{search}%")).all()

            return render_template('customers.html',
                                   customers=customers,
                                   form=form)


    return redirect('/')

@app.route('/create/route', methods = ["POST"])
def create_route():
    """add route to db"""
    form = RouteForm()

    if form.validate_on_submit():
        new_route = Route(name = form.name.data.lower())
        db.session.add(new_route)
        db.session.commit()
    
    return redirect('/admin/dashboard')


@app.route('/create/driver', methods = ['POST'])
def create_driver():
    """add new driver to db"""

    form = DriverForm()

    if form.validate_on_submit():
        new_driver = Driver.create(form.first_name.data.lower(),
                                   form.last_name.data.lower(),
                                   form.phone.data,
                                   form.username.data.lower(),
                                   form.password.data)
        db.session.commit()
    
    return redirect('/')

@app.route('/create/admin', methods=['POST'] )
def create_admin():
    """add admin to db"""

    form = AdminForm()

    if form.validate_on_submit():
        new_admin = Admin.create(form.first_name.data.lower(),
                                   form.last_name.data.lower(),
                                   form.phone.data,
                                   form.username.data.lower(),
                                   form.password.data)
        db.session.commit()

    return redirect('/')

@app.route('/select/driver/<route_id>', methods = ['POST'])
def select_driver(route_id):
    """select driver for route"""
    driver_id = request.form['driver']
    old_driver = Driver.query.filter_by(route_id=route_id).first()
    if old_driver:
        old_driver.route_id = Null()
        db.session.commit()

    if driver_id != '':
        driver = Driver.query.get(driver_id)
        driver.route_id = route_id
        db.session.commit()

    return redirect('/')

@app.route('/select/route/<stop_id>', methods =['POST'])
def select_route(stop_id):
    """select route for stop"""

    route_id = request.form['route']
    stop_id = stop_id
    stop = Stop.query.get(stop_id)

    if route_id != '':
        stop.route_id = route_id

    else:
        stop.route_id = Null()
    db.session.commit()

    return redirect('/')

@app.route('/select/status/<stop_id>', methods = ['POST'])
def change_status(stop_id):
    """ change status of stop """

    stop = Stop.query.get(stop_id)
    stop.status = request.form['status']
    db.session.commit()

    return redirect('/driver/opt_route')

@app.route('/customers/stops/<custy_id>', methods=["POST","GET"])
def add_stop(custy_id):
    """create new stop"""

    stop_form = StopForm()
    custy = Customer.query.get(custy_id)

    if stop_form.validate_on_submit():
        if stop_form.route_id.data == '0':
            new_stop = Stop(customer_id=custy_id,
                            start_time=stop_form.start_time.data,
                            end_time=stop_form.end_time.data)
        else:
            new_stop = Stop(customer_id=custy_id,
                            start_time=stop_form.start_time.data,
                            end_time=stop_form.end_time.data,
                            route_id=stop_form.route_id.data)
            
        db.session.add(new_stop)
        db.session.commit()
        return redirect('/customers')

    return render_template('stop-form.html', custy=custy, stop_form=stop_form)

@app.route('/create/customer', methods =['POST'])
def create_customer():
    """ create customer """

    form = CustomerForm()

    if form.validate_on_submit():
        new_cust = Customer.create(form.first_name.data.lower(),
                                   form.last_name.data.lower(),
                                   form.address.data.lower(),
                                   form.phone.data,
                                   form.email.data.lower(),
                                   form.doorman.data)
        db.session.commit()
    
    return redirect(f'/customers?q={form.first_name.data}')

@app.route('/route/<route_id>')
def show_route(route_id):
    """ show stops in route"""
    if g.user:
        route =  Route.query.get(route_id)
        
        return render_template('route.html',
                               route=route)
    
    return redirect('/')

@app.route('/route/<route_id>/<stop_id>', methods = ['POST'])
def remove_from_route(route_id,stop_id):
    """remove stop from route"""
    if g.user:
        stop = Stop.query.get(stop_id)
        stop.route_id = Null()
        db.session.commit()
        return redirect(f'/route/{route_id}')
    
    return redirect('/')

@app.route('/delete/<model>/<id>', methods=['POST'])
def handle_delete(model,id):

    if g.user:
        if model == 'Driver':
            Driver.query.filter_by(id=id).delete()
        if model == 'Route':
            Route.query.filter_by(id=id).delete()
        if model == 'Stop':
            Stop.query.filter_by(id=id).delete()
        if model == 'Admin':
            Admin.query.filter_by(id=id).delete()
        if model == 'Customer':
            Customer.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect('/customers')


        db.session.commit()
    
    return redirect('/')