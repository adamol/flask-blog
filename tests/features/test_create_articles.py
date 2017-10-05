import unittest
from tests.base import BaseTestCase
from app import db
from models.Article import Article
from models.User import User

class CreateArticleTest(BaseTestCase):

    def test_admins_can_create_new_articles(self):
        response = self.asAdmin().client.post("/articles/", data={
            "title": "New Title", "body": "Some body content", "tag": "PHP"
        }, follow_redirects=True)

        self.assertIn(b'New Title', response.data)

        article = Article.query.first()
        self.assertEqual('Some body content', article.body)

    def test_non_admins_cannot_create_new_articles(self):
        user = User("john", "john@example.com", "secret")

        response = self.asUser(user).client.post("/articles/", data={
            "title": "New Title", "body": "Some body content", "tag": "PHP"
        }, follow_redirects=True)

        self.assertIn(b'must be an admin', response.data)

    def test_title_is_required_to_create_a_article(self):
        response = self.asAdmin().client.post("/articles/", data={
            "body": "Some body content", "tag": "PHP"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

    def test_body_is_required_to_create_a_article(self):
        response = self.asAdmin().client.post("/articles/", data={
            "title": "New Title", "tag": "PHP"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

    def test_tag_is_required_to_create_a_article(self):
        response = self.asAdmin().client.post("/articles/", data={
            "title": "New Title", "body": "Some body content"
        }, follow_redirects=True)

        self.assertIn(b'Bad Request', response.data)

if __name__ == '__main__':
    unittest.main()