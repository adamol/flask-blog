from flask_testing import TestCase
from app import app, db
from models.User import User
from passlib.hash import sha256_crypt

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def asAdmin(self):
        return self.asUser(User("admin", "admin@example.com", "admin"))

    def asUser(self, user):
        db.session.add(
            User(user.username, user.email, sha256_crypt.hash(user.password))
        )

        self.client.post('/auth/login', data={
            "username": user.username, "password": user.password,
        }, follow_redirects=True)

        return self


