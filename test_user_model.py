"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_user_model.py


import os
from unittest import TestCase
from flask import g

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test User Model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.__repr__(), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_follows(self):
        """Does user follows work as expected?"""

        u1 = User(
            email="first@user.com",
            username="firsttestuser",
            password="HASHED_PASS"  
        )

        u2 = User(
            email="second@user.com",
            username="secondtestuser",
            password="HASHED_PASS"
        )

        db.session.add_all([u1, u2])
        db.session.commit()
        
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

        follow1 = Follows(user_being_followed_id = u1.id, user_following_id = u2.id)
        follow2 = Follows(user_being_followed_id = u2.id, user_following_id = u1.id)
        db.session.add_all([follow1, follow2])
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_following(u1))
        
    def test_user_validation(self):
        """Assure username is unique upon signup + verify login validation"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="PASSWORD"
        )

        hashed_user = u.signup(username=u.username, email = u.email, password = u.password, image_url = None)
        self.assertIsInstance(hashed_user, User)

        db.session.add(hashed_user)
        db.session.commit()
        
        logged_in = hashed_user.authenticate(username = u.username, password = u.password)
        self.assertIsInstance(logged_in, User)

        bad_user = hashed_user.authenticate(username = u.username, password = "not it")
        bad_user2 = hashed_user.authenticate(username = "This also isn't it", password = u.password)
        self.assertFalse(bad_user)
        self.assertFalse(bad_user2)

        # username, email, password, image_url