"""
BaseTest

This class creates a parent class for each non-unit test.
Instantiates a new, blank database each test.
"""

from unittest import TestCase
from app import app
from db import db


class IntegrationBaseTest(TestCase):
    def setUp(self) -> None:
        # Make sure db exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.init_app(app)
            db.create_all()
        # Get a test client
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Db is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
