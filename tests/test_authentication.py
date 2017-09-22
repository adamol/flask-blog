import unittest
from base import BaseTestCase
from models.User import User
from passlib.hash import sha256_crypt
from app import db

class AuthenticationTest(BaseTestCase):

    def test_guests_can_register(self):
        self.client.post('/auth/register', data={
            "username": "john",
            "email": "john@example.com",
            "password": "secret",
            "confirm_password": "secret",
        }, follow_redirects=True)

        user = User.query.filter_by(username="john").first()
        self.assertEqual("john@example.com", user.email)
        if not sha256_crypt.verify("secret", user.password):
            raise Exception

    def test_users_can_login(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        response = self.client.post('/auth/login', data={
            "username": "john",
            "password": "secret",
        }, follow_redirects=True)

        self.assertIn(b'john', response.data)

    def test_username_must_match_records(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        response = self.client.post('/auth/login', data={
            "username": "jane", "password": "secret",
        }, follow_redirects=True)

        self.assertIn(b'No user with that username', response.data)

    def test_password_must_match_records(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        response = self.client.post('/auth/login', data={
            "username": "john", "password": "incorrect-password",
        }, follow_redirects=True)

        self.assertIn(b'Password did not match our records.', response.data)

    def test_logging_out_destroy_session(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        self.client.post('/auth/login', data={
            "username": "john", "password": "secret",
        }, follow_redirects=True)

        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'logged out', response.data)

if __name__ == '__main__':
    unittest.main()
