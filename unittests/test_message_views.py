
import os
from unittest import TestCase
from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False
app.config['Testing'] = True


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_add_message_logged_in(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_delete_message_logged_in(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            c.post("/messages/new", data={"text": "Hello"})
            msg = Message.query.one()
            resp = c.post(f'messages/{msg.id}/delete')
            messages = Message.query.all()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(messages, [])

    def test_add_message_invalid_user(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = 9876
            resp = self.client.post('/messages/new', data={"text": "test"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)

    def test_add_message_not_logged_in(self):

        resp = self.client.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
        html = resp.get_data(as_text=True)
        msg = Message.query.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(msg, [])
        self.assertIn('Access unauthorized', html)

    def test_delete_message_invalid_user(self):

        u = User.signup('username', 'fake@fake.com', 'password', image_url=None)
        u.id = 999
        msg = Message(id=123, text='This is a test', user_id=self.testuser.id)

        db.session.add_all([u, msg])
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = 999
            resp = self.client.post(f'/messages/{msg.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            messages = Message.query.get(msg.id)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(messages, msg)
            self.assertIn('Access unauthorized', html)

    def test_delete_message_not_logged_in(self):

        msg = Message(text='This is a test', user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        resp = self.client.post(f'/messages/{msg.id}/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        messages = Message.query.get(msg.id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', html)
        self.assertEqual(msg, messages)

    
        