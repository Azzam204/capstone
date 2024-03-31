"""Models tests."""

# run these tests like:
#
#    python -m unittest test_models.py

import os
from unittest import TestCase
from datetime import time

from models import db , Route, Stop, Driver, Customer, Admin


os.environ['DATABASE_URL'] = "postgresql:///deliverease-test"

from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

class AdminModelTestCase(TestCase):
    """ Test admin model """

    def setUp(self):

        with app.app_context():

            Admin.query.delete()

            db.session.commit()
            
            self.client = app.test_client()

    def test_admin_creation(self):
        """ Does Admin.create() work? """

        with app.app_context():
            admin = Admin.create('test','testarony',1234567890,'test204','password')

            db.session.commit()

        self.assertEqual(admin.username,'test204')

        with self.assertRaises(TypeError):
            Admin.create('test','testarony')

    def test_admin_authentication(self):
        """ Does Admin.authenticate() work? """
        
        with app.app_context():
            admin = Admin.create('test','testarony',1234567890,'test204','password')

            db.session.commit()

            self.assertEqual(Admin.authenticate('test204','password'),admin)
            self.assertEqual(Admin.authenticate('test204','passwrd'),False)
            self.assertEqual(Admin.authenticate('test','password'),False)


class RouteModelTestCase(TestCase):
    """ Test route model """

    def setUp(self):

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            db.session.commit()
            
            self.client = app.test_client()

    def test_route_creation(self):
        """ does basic model work"""

        with app.app_context():
            route = Route(name='testtown')
            db.session.add(route)
            db.session.commit()

            self.assertEqual(route.name,'testtown')



class DriverModelTestCase(TestCase):
    """ Test driver model """

    def setUp(self):

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            db.session.commit()
            
            self.client = app.test_client()

    def test_driver_creation(self):
        """ Does Driver.create() work? """

        with app.app_context():
            driver = Driver.create('test','testarony',1234567890,'test204','password')

            db.session.commit()

        self.assertEqual(driver.username,'test204')

        with self.assertRaises(TypeError):
            driver.create('test','testarony')

    def test_driver_authentication(self):
        """ Does Driver.authenticate() work? """
        
        with app.app_context():
            driver = Driver.create('test','testarony',1234567890,'test204','password')

            db.session.commit()

            self.assertEqual(Driver.authenticate('test204','password'),driver)
            self.assertEqual(Driver.authenticate('test204','passwrd'),False)
            self.assertEqual(Driver.authenticate('test','password'),False)

    def test_driver_route_relation(self):
        """ Do the relationships work?"""

        with app.app_context():

            driver = Driver.create('test','testarony',1234567890,'test204','password') 

            route = Route(name='testtown')

            db.session.add(route)
            db.session.commit()

            driver.route_id = route.id

            db.session.commit()

            self.assertEqual(driver.route, route)
            self.assertEqual(driver.route.name,'testtown')

class CustomerModelTestCase(TestCase):
    """ Test customer model """

    def setUp(self):

        with app.app_context():

            Admin.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Driver.query.delete()
            Route.query.delete()

            db.session.commit()
            
            self.client = app.test_client()

    def test_customer_creation(self):
        """ does Customer.create() work?"""

        with app.app_context():

            customer = Customer.create('test','testomer','123 main street',1234567890,'test204@gmail.com')

            db.session.commit()

            self.assertEqual(customer.first_name,'test')

            with self.assertRaises(TypeError):
                customer.create('test','testarony')

    def test_customer_stop_relation(self):
        """ does customer.stop work?"""

        with app.app_context():

            customer = Customer.create('test','testomer','123 main street',1234567890,'test204@gmail.com')

            db.session.commit()

            test_stop = Stop(customer_id = customer.id,
                             start_time = time(18),
                             end_time = time(21))
            
            db.session.add(test_stop)
            db.session.commit()

            self.assertEqual(customer.stops,[test_stop])
            self.assertEqual(test_stop.customer,customer)
    


class StopModelTestCase(TestCase):
    """ Test stop model """
    
    def setUp(self):

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            db.session.commit()
            
            self.client = app.test_client()

    def test_stop_route_relation(self):

        with app.app_context():

            customer = Customer.create('test','testomer','123 main street',1234567890,'test204@gmail.com')

            route = Route(name ='testtown')

            db.session.add(route)
            db.session.commit()

            test_stop = Stop(customer_id = customer.id,
                             start_time = time(18),
                             end_time = time(21),
                             route_id = route.id)
            
            db.session.add(test_stop)
            db.session.commit()

            self.assertEqual(route.stops,[test_stop])
            self.assertEqual(test_stop.route,route)
