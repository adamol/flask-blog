import unittest
from tests.base import BaseTestCase
from app import db
from models.Article import Article
from models.User import User
from passlib.hash import sha256_crypt

class CreateCommentsTest(BaseTestCase):

    def test_guests_cannot_article_a_comment(self):
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        article = Article.query.first()

        response = self.client.post("/articles/"+str(article.id)+"/comments", data={
            "body": "test comment"
        }, follow_redirects=True)

        self.assertIn(b'must be logged in to article a comment.', response.data)

    def test_logged_in_users_can_article_comments(self):
        db.session.add(Article("Some Title", "Lorem ipsum dolor sit amet", 1))
        article = Article.query.first()

        db.session.add(User("john","john@example.com", sha256_crypt.hash("secret")))
        self.client.post('/auth/login', data={
            "username": "john", "password": "secret",
        }, follow_redirects=True)

        response = self.client.post("/articles/"+str(article.id)+"/comments", data={
            "body": "test comment"
        }, follow_redirects=True)

        self.assertIn(b'test comment', response.data)
