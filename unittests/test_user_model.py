import os
from unittest import TestCase
from pdb import set_trace
from models import db, User, Message, Follows
from sqlalchemy import exc

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="example@example.com",
            username="exampleuser",
            password="SECURE_PASSWORD"
        )
        u2.followers.append(u)

        db.session.add_all([u, u2])
        db.session.commit()

        # User should have no messages & no followers, following one
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 1)

        # Test __repr__ method on users
        self.assertEqual(str(u), f'<User #{u.id}: {u.username}, {u.email}>')

        # User 1 should be following User 2
        self.assertTrue(u.is_following(u2))
        self.assertTrue(u2.is_followed_by(u))
        self.assertFalse(u2.is_following(u))
        self.assertFalse(u.is_followed_by(u2))

    def test_valid_signup(self):
        '''Does User.signup create/fail to create user based on validations?'''
        valid_u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        # User is added to session within signup method
        db.session.commit()
        self.assertIsNotNone(valid_u)

    def test_invalid_signup(self):

        invalid_u = User.signup(
            email=None,
            username='noemailuser',
            password="failed_email",
            image_url=None
        )

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_authentication(self):

        valid_u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        auth_check_valid = User.authenticate('testuser', 'HASHED_PASSWORD')
        auth_check_invalid_username = User.authenticate('invalid_username', 'HASHED_PASSWORD')
        auth_check_invalid_password = User.authenticate('testuser', 'invalid_password')

        self.assertEqual(auth_check_valid, valid_u)
        self.assertFalse(auth_check_invalid_username)
        self.assertFalse(auth_check_invalid_password)

    
    



        







