from unittest import TestCase
from fujiserver import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Login Page", result.data)

    def test_register(self):
        """Test register page.""" 

        result = self.client.get("/register")
        self.assertIn(b"<h1>Register</h1>", result.data)

    
    def test_feedpage(self):
        """Test feedpage form, test form not suppose to show: not logged in."""

        result = self.client.get("/feedpage")
        self.assertNotIn(b"<h1>Register</h1>", result.data)
        

class TestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        # Call add example_data function only in testing. Not in fuji DB.
        example_data()

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "cat@cat.com", "password": "4321"},
                                  follow_redirects=True)
        self.assertIn(b"<h2>cat, Welcome to Fuji Chat</h2>", result.data)

        result_1 = self.client.post("/login",
                                  data={"email": "cat@cat.com", "password": "2345"},
                                  follow_redirects=True)
        self.assertIn(b"Invalid password, please try again!", result_1.data)

        result_2 = self.client.post("/login",
                                  data={"email": "catli@cat.com", "password": "1234"},
                                  follow_redirects=True)
        self.assertIn(b"<h1>Register</h1>", result_2.data)


    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b'You are logged out, see you soon.', result.data)

    def test_db(self):
        """Test data added to db"""

        result = self.client.post("/register",
                                  data={"email": "miao@miao.com", "password": "0000",
                                        "fname": "miao", "lname": "miao", "language": "en"},
                                  follow_redirects=True)

        self.assertIn(b"<h2>Login</h2>", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    import unittest

    unittest.main()