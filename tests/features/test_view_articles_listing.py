import unittest
from tests.base import BaseTestCase
from app import db
from models.Article import Article
from models.Article import Tag
from models.User import User
from passlib.hash import sha256_crypt

class ViewArticlesListingTest(BaseTestCase):

    def test_users_can_view_articles(self):
        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        db.session.add(Article("Another Title", "Doesnt matter", 1))

        response = self.client.get('/articles/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Some Title', response.data)
        self.assertIn(b'Another Title', response.data)

    def test_users_can_filter_articles_by_tag(self):
        tagA  = Tag("PHP")
        tagB  = Tag("JavaScript")
        user  = User("john","john@example.com", sha256_crypt.hash("secret"))
        articleA = Article("First PHP Article", "Lorem ipsum dolor sit amet", 1)
        articleB = Article("JavaScript Article", "Should not be visible", 1)
        articleC = Article("Second PHP Article", "Lorem ipsum dolor sit amet", 1)
        articleA.tags.append(tagA)
        articleB.tags.append(tagB)
        articleC.tags.append(tagA)
        user.articles.extend([articleA,articleB,articleC])
        db.session.add(user)
        db.session.add_all([articleA, articleB, articleC])
        db.session.add_all([tagA, tagB])

        response = self.client.get('/articles/?tags=php', content_type='html/text')
        self.assertIn(b'First PHP Article', response.data)
        self.assertIn(b'Second PHP Article', response.data)
        self.assertNotIn(b'JavaScript Article', response.data)

if __name__ == '__main__':
    unittest.main()
