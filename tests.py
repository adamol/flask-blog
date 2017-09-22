from app import app, db
from flask_testing import TestCase
from flask import session
import unittest
from passlib.hash import sha256_crypt
from models.User import User
from models.Post import Post
from models.Comment import Comment

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class IndexTest(BaseTestCase):

    def test_index_loads_correctly(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

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


class ViewPostsListingTest(BaseTestCase):

    def test_users_can_view_posts(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))
        db.session.add(Post("Some Title", "Lorem ipsum dolor sit amet", 1))
        db.session.add(Post("Another Title", "Doesnt matter", 1))

        response = self.client.get('/posts/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Some Title', response.data)
        self.assertIn(b'Another Title', response.data)


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

class ViewPostDetailsTest(BaseTestCase):

    def test_guests_can_view_a_single_post(self):
        db.session.add(User("admin","admin@example.com", sha256_crypt.hash("admin")))
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))

        admin = User.query.filter_by(username="admin").first()
        db.session.add(Post("Some Title", "Lorem ipsum dolor sit amet", admin.id))

        john  = User.query.filter_by(username="john").first()
        post = Post.query.first()
        db.session.add(Comment(post.id, john.id, "Nice post!"))

        response = self.client.get('/posts/'+str(post.id), content_type='html/text')

        self.assertIn(b'Some Title', response.data)
        self.assertIn(b'Lorem ipsum dolor sit amet', response.data)
        self.assertIn(b'admin', response.data)
        self.assertIn(b'Nice post!', response.data)
        self.assertIn(b'john', response.data)

class CreateCommentsTest(BaseTestCase):

    def test_guests_cannot_post_a_comment(self):
        db.session.add(Post("Some Title", "Lorem ipsum dolor sit amet", 1))
        post = Post.query.first()

        response = self.client.post("/posts/"+str(post.id)+"/comments", data={
            "body": "test comment"
        }, follow_redirects=True)

        self.assertIn(b'must be logged in to post a comment.', response.data)

    def test_logged_in_users_can_post_comments(self):
        db.session.add(Post("Some Title", "Lorem ipsum dolor sit amet", 1))
        post = Post.query.first()

        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))
        self.client.post('/auth/login', data={
            "username": "john", "password": "secret",
        }, follow_redirects=True)

        response = self.client.post("/posts/"+str(post.id)+"/comments", data={
            "body": "test comment"
        }, follow_redirects=True)

        self.assertIn(b'test comment', response.data)

if __name__ == '__main__':
    unittest.main()
