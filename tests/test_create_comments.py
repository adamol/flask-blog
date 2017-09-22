import unittest
from base import BaseTestCase
from app import db
from models.Post import Post
from models.User import User
from passlib.hash import sha256_crypt

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
