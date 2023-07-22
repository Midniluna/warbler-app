"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask import g

from models import db, User, Message, Likes

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

class MessageModelTestCase(TestCase):

    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

        u = User.signup("testuser", "test@test.com", "password", None
        )

        db.session.add(u)
        db.session.commit()

        self.user = u

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    

    def test_message_model(self):
        """Confirm message model works as intended"""

        msg = Message(
            text = "Mmm content",
            user_id = self.user.id
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "Mmm content")

    def test_message_likes(self):
        """Confirm liking a message works as intended"""

        user2 = User.signup("anotheruser", "email@em.com", "password", None)

        db.session.add(user2)
        db.session.commit()

        msg = Message(
            text = "Wowie new message",
            user_id = self.user.id
        )

        db.session.add(msg)
        db.session.commit()

        user2.likes.append(msg)
        db.session.commit()

        l = Likes.query.filter(Likes.user_id == user2.id).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, msg.id)