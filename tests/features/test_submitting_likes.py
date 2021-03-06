import unittest
from tests.base import BaseTestCase
from project.models import Article
from app import db

class SubmittingLikesTest(BaseTestCase):

    def test_users_can_like_an_article(self):
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        article = Article.query.first()
        response = self.asAdmin().client.post(
            "/articles/"+str(article.id)+"/likes", data={}, follow_redirects=True
        )
        self.assertIn(b'Some Title', response.data) # assert redirect back
        self.assertEqual(1, len(article.likes))

    def test_users_can_toggle_a_like(self):
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        article = Article.query.first()
        response = self.asAdmin().client.post(
            "/articles/"+str(article.id)+"/likes", data={}, follow_redirects=True
        )
        response = self.client.post(
            "/articles/"+str(article.id)+"/likes", data={}, follow_redirects=True
        )
        self.assertEqual(0, len(article.likes))

    def test_guests_cannot_like_an_article(self):
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        article = Article.query.first()
        response = self.client.post(
            "/articles/"+str(article.id)+"/likes", data={}, follow_redirects=True
        )
        self.assertEqual(0, len(article.likes))
        self.assertIn(b'Guests cannot submit likes.', response.data)

    #def test_users_can_like_a_comment(self):

    # def test_guests_cannot_like_a_comment(self):

if __name__ == '__main__':
    unittest.main()
