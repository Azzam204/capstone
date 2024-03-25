"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db , app
from models import Driver, Admin, Customer


with app.app_context():
    db.drop_all()
    db.create_all()

    with open('generator/admins.csv') as admins:
        db.session.bulk_insert_mappings(Admin, DictReader(admins))

    with open('generator/customers.csv') as customers:
        db.session.bulk_insert_mappings(Customer, DictReader(customers))

    with open('generator/drivers.csv') as drivers:
        db.session.bulk_insert_mappings(Driver, DictReader(drivers))

    db.session.commit()
