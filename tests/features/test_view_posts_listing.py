import unittest
from tests.base import BaseTestCase
from app import db
from models.Post import Post
from models.Post import Tag
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

    def test_users_can_filter_posts_by_tag(self):
        tagA  = Tag("php")
        tagB  = Tag("javascript")
        user  = User("john","john@example.com", sha256_crypt.hash("secret"))
        postA = Post("First PHP Article", "Lorem ipsum dolor sit amet", 1)
        postB = Post("JavaScript Article", "Should not be visible", 1)
        postC = Post("Second PHP Article", "Lorem ipsum dolor sit amet", 1)
        postA.tags.append(tagA)
        postB.tags.append(tagB)
        postC.tags.append(tagA)
        user.posts.extend([postA,postB,postC])
        db.session.add(user)
        db.session.add_all([postA, postB, postC])
        db.session.add_all([tagA, tagB])

        response = self.client.get('/posts/?tags=php', content_type='html/text')
        self.assertIn(b'First PHP Article', response.data)
        self.assertIn(b'Second PHP Article', response.data)
        self.assertNotIn(b'JavaScript Article', response.data)

if __name__ == '__main__':
    unittest.main()
