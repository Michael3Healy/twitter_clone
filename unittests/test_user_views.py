
import os
from unittest import TestCase
from models import db, connect_db, Message, User, Follows, Likes
from pdb import set_trace

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

        self.testmessage = Message(text='testing', user_id=self.testuser.id)

        db.session.add(self.testmessage)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_add_like(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        resp = self.client.post(f'/users/add_remove_like/{self.testmessage.id}', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(len(self.testuser.likes), 1)
        self.assertEqual(resp.status_code, 200)

    def test_remove_like(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        like_message = Likes(user_id=self.testuser.id, message_id=self.testmessage.id)
        db.session.add(like_message)
        db.session.commit()

        resp = self.client.post(f'/users/add_remove_like/{self.testmessage.id}', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(len(self.testuser.likes), 0)
        self.assertEqual(resp.status_code, 200)

    def test_show_user(self):

        resp = self.client.get(f'/users/{self.testuser.id}', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.testuser.username, html)

    def test_show_following(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        u = User.signup(
                username='followeduser', 
                password='password', 
                email='testing@test.com', 
                image_url=None)
        db.session.commit()
        
        follow = Follows(user_being_followed_id=u.id, user_following_id=self.testuser.id)
        db.session.add(follow)
        db.session.commit()

        resp = self.client.get(f'/users/{self.testuser.id}/following', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(u.username, html)

    def test_show_followers(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        u = User.signup(
                username='followeduser', 
                password='password', 
                email='testing@test.com', 
                image_url=None)
        db.session.commit()
        
        follow = Follows(user_being_followed_id=self.testuser.id, user_following_id=u.id)
        db.session.add(follow)
        db.session.commit()

        resp = self.client.get(f'/users/{self.testuser.id}/followers', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(u.username, html)

    def test_update_profile(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        resp = self.client.post(f'/users/profile', data={"username": "Michael", "password": "testuser", "bio": "New Bio"}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Michael', html)

    def test_delete_user(self):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

        resp = self.client.post(f'/users/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)

        deleted_user = User.query.get(self.testuser.id)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(deleted_user)

    def test_update_profile_unauthorized(self):
        resp = self.client.post(f'/users/profile', data={"username": "Michael", "password": "testuser", "bio": "New Bio"}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', html)

    def test_add_like_no_validation(self):
        resp = self.client.post(f'/users/add_remove_like/{self.testmessage.id}', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(len(self.testuser.likes), 0)
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Access unauthorized', html)


            

    
    
        