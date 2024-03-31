"""Views tests."""

# run these tests like:
#
#    python -m unittest test_views.py

import os
from unittest import TestCase
from datetime import time
from api import *

from models import db , Route, Stop, Driver, Customer, Admin


os.environ['DATABASE_URL'] = "postgresql:///deliverease-test"

from app import app, CUR_USER , USER_TYPE, admin_type, driver_type 

with app.app_context():
    db.drop_all()
    db.create_all()


app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True


class LoggedOutTestCase(TestCase):
    """ Test views for admin """

    def setUp(self):
        """create test client. """
        self.client = app.test_client()

    def test_loggedout_home(self):
        """ can we reach log in page """

        with self.client as c:
            resp = c.get('/',
                         follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Login',html)


    def test_loggedout_admindash(self):
        """ are we redirected if we attempt to view admin dash while logged out """

        with self.client as c:
            resp = c.get('/admin/dashboard',
                         follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Access unauthorized', html)


    def test_loggedout_driverdash(self):
        """ are we redirected if we attempt to view driver dash while logged out """

        with self.client as c:
            resp = c.get('/driver/dashboard',
                         follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Access unauthorized', html)


    def test_loggedout_customers(self):
        """ are we redirected if we attempt to view customers while logged out """

        with self.client as c:
            resp = c.get('/customers',
                         follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Access unauthorized', html)

    
class DriverViewsTestCase(TestCase):
    """ Test views for admin """

    def setUp(self):
        """create test client, add sample data."""

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            self.client = app.test_client()

            self.testdriver = Driver.create('testfirst',
                                          'testlast',
                                          1234567890,
                                          'test204',
                                          'password')
            db.session.commit()

    def test_driverdash_redirect(self):
        """does home redirect to driver dash if driver in session"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testdriver.id
                sess[USER_TYPE] = driver_type

            resp = c.get('/',
                         follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('No stops yet!',html)


    def test_driverdash_route(self):
        """does driver dash display driver route"""
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

            driver = Driver.query.get(self.testdriver.id)

            driver.route_id = route.id

            db.session.commit()
            

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testdriver.id
                sess[USER_TYPE] = driver_type

            resp = c.get('/',
                         follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testtown',html)
            self.assertIn('Test Testomer',html)


class AdminViewsTestCase(TestCase):
    """ Test views for admin """

    def setUp(self):
        """create test client, add sample data."""

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            self.client = app.test_client()

            self.testadmin = Admin.create('testfirst',
                                          'testlast',
                                          1234567890,
                                          'test204',
                                          'password')
            
            self.testdriver = Driver.create('testdriverfirst',
                                          'testlast',
                                          1234567890,
                                          'testiver204',
                                          'password')
            db.session.commit()


    def test_admindash_redirect(self):
        """does home redirect to admin dash if admin in session"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type

            resp = c.get('/',
                         follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Routes',html)
            self.assertIn('Stops',html)
            self.assertIn('Drivers',html)


    def test_admindash_shows_data(self):
        """does admin dash display stops, routes, drivers"""

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

            driver = Driver.query.get(self.testdriver.id)

            driver.route_id = route.id

            db.session.commit()
            

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type

            resp = c.get('/admin/dashboard')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testomer',html)
            self.assertIn('Testdriverfirst',html)
            self.assertIn('Testtown',html)

    
    def test_customers_view(self):
        """can I view customers"""

        with app.app_context():

            customer = Customer.create('test','testomer','123 main street',1234567890,'test204@gmail.com')

            db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type

            resp = c.get('/customers')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testomer',html)           


class PostRoutesTestCase(TestCase):
    """ test create routes """

    def setUp(self):
        """create test client, add sample data."""

        with app.app_context():

            Admin.query.delete()
            Driver.query.delete()
            Stop.query.delete()
            Customer.query.delete()
            Route.query.delete()

            self.client = app.test_client()

            self.testadmin = Admin.create('testfirst',
                                          'testlast',
                                          1234567890,
                                          'test204',
                                          'password')
            
            db.session.commit()
    
    def test_create_driver(self):
        """ does create driver view work"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type
            
            data = {'first_name':'testfirst',
                    'last_name':'testlast',
                    'phone':1234567890,
                    'username':'test204',
                    'password':'password'}
            
            resp = c.post('/create/driver',
                          data=data,
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testfirst',html)


    def test_create_route(self):
        """ does create route view work"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type
            
            data = {'name':'testtown'}
            
            resp = c.post('/create/route',
                          data=data,
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testtown',html)


    def test_create_customer(self):
        """ does create customer view work"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CUR_USER] = self.testadmin.id
                sess[USER_TYPE] = admin_type
            
            data = {'first_name':'testfirst',
                    'last_name':'testlast',
                    'address':'123 main street',
                    'phone':1234567890,
                    'email':'test204@gmail.com',
                    'doorman':'False'}
            
            resp = c.post('/create/customer',
                          data=data,
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Testfirst',html)
