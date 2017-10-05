import unittest
from tests.base import BaseTestCase
from app import db
from models.Post import Post
from models.User import User

class CreatePostsTest(BaseTestCase):

    def test_admins_can_create_new_posts(self):
        response = self.asAdmin().client.post("/posts/", data={
            "title": "New Title", "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'New Title', response.data)

        post = Post.query.first()
        self.assertEqual('Some body content', post.body)

    def test_non_admins_cannot_create_new_posts(self):
        user = User("john", "john@example.com", "secret")

        response = self.asUser(user).client.post("/posts/", data={
            "title": "New Title", "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'must be an admin', response.data)

    def test_title_is_required_to_create_a_post(self):
        response = self.asAdmin().client.post("/posts/", data={
            "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

    def test_body_is_required_to_create_a_post(self):
        response = self.asAdmin().client.post("/posts/", data={
            "title": "New Title"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

if __name__ == '__main__':
    unittest.main()
