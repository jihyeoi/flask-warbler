"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_is_following(self):
        """testing if user1 is following user2"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(len(u2.followers), 1)

    def test_is_not_following(self):
        """user1 is not following user2"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(len(u2.followers), 0)

    def test_is_followed_by(self):
        """testing if user1 is followed by user2"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)

        self.assertTrue(u1.is_followed_by(u2))
        self.assertEqual(len(u1.followers), 1)

    def test_is_not_followed_by(self):
        """user1 is not followed by user2"""
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))
        self.assertEqual(len(u1.followers), 0)

    def test_user_signup_success(self):
        """successfully create a new user given valid credentials"""

        user1 = User.signup(
            username="user1",
            email="user1@gmail.com",
            password="123456"
        )

        db.session.commit()

        users = User.query.all()

        self.assertIn(user1, users)
        self.assertIsInstance(user1, User)

    def test_user_signup_fail(self):
        """unsuccessfully create a new user given invalid credentials"""

        # if we want to test a function and it should raise an error
        # we have to use a with block & self.assertRaises
        # the with block will automatically clean up after

        with self.assertRaises(IntegrityError):
            User.signup(
                username="u1",
                email="",
                password="123456"
            )

            db.session.commit()

        # tool called coverage:
        # runs all tests, checks to see how much % of our code was tested
        # pip3 install coverage
        # coverage run -m unittest
        # coverage report
        # coverage html

    def test_user_authenticate_success(self):
        """successfully authenticates a user when given a valid username & password"""

        # dont need to make an instance of u1
        # we are testing for authenticate so we can just pass in values

        auth_result = User.authenticate("u1", "password")
        u1 = User.query.get(self.u1_id)

        self.assertEqual(auth_result, u1)
        self.assertIsInstance(auth_result, User)


    def test_user_authenticate_fail_username(self):
        """
            unsuccessfully authenticates a user
            when given an invalid username but valid password
        """
        auth_result = User.authenticate(username="u4", password="password")
        u1 = User.query.get(self.u1_id)

        self.assertFalse(auth_result)
        self.assertNotEqual(auth_result, u1)


    def test_user_authenticate_fail_password(self):
        """
            unsuccessfully authenticates a user
            when given an valid username but invalid password
        """
        auth_result = User.authenticate(username="u1", password="booooooooo")
        u1 = User.query.get(self.u1_id)

        self.assertFalse(auth_result)
        self.assertNotEqual(auth_result, u1)







