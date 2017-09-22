import unittest
from base import BaseTestCase
from app import db
from models.Post import Post
from models.User import User
from passlib.hash import sha256_crypt

class CreatePostsTest(BaseTestCase):

    def test_admins_can_create_new_posts(self):
        db.session.add(User("admin","admin@example.com", sha256_crypt.hash("admin")))

        self.client.post('/auth/login', data={
            "username": "admin", "password": "admin",
        }, follow_redirects=True)

        response = self.client.post("/posts/", data={
            "title": "New Title", "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'New Title', response.data)

        post = Post.query.first()
        self.assertEqual('Some body content', post.body)

    def test_non_admins_cannot_create_new_posts(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        self.client.post('/auth/login', data={
            "username": "john", "password": "secret",
        }, follow_redirects=True)

        response = self.client.post("/posts/", data={
            "title": "New Title", "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'must be an admin', response.data)

    def test_title_is_required_to_create_a_post(self):
        db.session.add(User("admin","admin@example.com", sha256_crypt.hash("admin")))

        self.client.post('/auth/login', data={
            "username": "admin", "password": "admin",
        }, follow_redirects=True)

        response = self.client.post("/posts/", data={
            "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

    def test_body_is_required_to_create_a_post(self):
        db.session.add(User("admin","admin@example.com", sha256_crypt.hash("admin")))

        self.client.post('/auth/login', data={
            "username": "admin", "password": "admin",
        }, follow_redirects=True)

        response = self.client.post("/posts/", data={
            "title": "New Title"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

if __name__ == '__main__':
    unittest.main()
