from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config["DATABASE_URL"] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first", last_name="test_last", image_url=None)

        second_user = User(first_name="Kate", last_name="Moser", image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.second_user_id = second_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_new_user_form(self):
        """Tests request to display new user form"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("NEW USER FORM DO NOT DELETE", html)

    def test_process_form_and_add_user(self):
        """Tests process form and add user"""
        with self.client as c:
            resp = c.post(
                "/users/new",
                data={
                    "first-name": "new_first_name",
                    "last-name": "new_last_name",
                    "image-url": "https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg",
                },
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)
            # add test for errors after adding error handling
            self.assertIn("new_first_name", html)
            self.assertIn("new_last_name", html)

    def test_display_user_info(self):
        """Tests display user info page"""

        with self.client as c:
            resp = c.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)
            # REVIEW: also check something else, more unique to page
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_edit_user(self):
        """Tests edit user form submission"""
        with self.client as c:
            resp = c.post(
                f"/users/{self.user_id}/edit",
                data={
                    "first-name": "edit_first",
                    "last-name": "edit_last",
                    "image-url": "https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg",
                },
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)
            self.assertIn("edit_first", html)
            self.assertIn("edit_last", html)

    def test_process_form_and_delete(self):
        """Tests process form and delete user"""
        with self.client as c:
            resp = c.post(f"users/{self.second_user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Kate", html)
            self.assertNotIn("Moser", html)
