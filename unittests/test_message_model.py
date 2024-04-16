import os
from unittest import TestCase
from models import db, User, Message, Likes
from datetime import datetime
from pdb import set_trace

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Likes.query.delete()

        self.test_user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(self.test_user)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text='This is a test', user_id=self.test_user.id)
        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.user, self.test_user)
        self.assertEqual(self.test_user.messages[0], m)
        self.assertEqual(self.test_user.messages[0].text, 'This is a test')

    def test_message_likes(self):
        m = Message(text='This is a test', user_id=self.test_user.id)
        db.session.add(m)
        db.session.commit()
        
        self.test_user.likes.append(m)

        likes = Likes.query.filter(Likes.user_id == self.test_user.id).all()
        
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].message_id, m.id)


    