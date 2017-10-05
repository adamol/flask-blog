import unittest
from tests.base import BaseTestCase
from app import db
from models.Post import Post
from models.User import User
from passlib.hash import sha256_crypt

class ViewPostsListingTest(BaseTestCase):

    def test_users_can_view_posts(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))
        db.session.add(Post("Some Title", "Lorem ipsum dolor sit amet", 1))
        db.session.add(Post("Another Title", "Doesnt matter", 1))

        response = self.client.get('/posts/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Some Title', response.data)
        self.assertIn(b'Another Title', response.data)

if __name__ == '__main__':
    unittest.main()
