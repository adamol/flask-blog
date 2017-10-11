import unittest
from tests.base import BaseTestCase
from app import db
from models.Article import Article
from models.Article import Tag
from models.User import User
from tests.factories import ArticleFactory

class ViewArticlesListingTest(BaseTestCase):

    def test_users_can_view_articles(self):
        articles = [ArticleFactory.create() for i in range(2)]

        response = self.client.get('/articles/', content_type='html/text')

        for article in articles:
            self.assertIn(article.title, response.data)

    def test_users_can_filter_articles_by_tag(self):
        db.session.add_all([Tag(tag) for tag in ["php", "javascript"]])
        articleA = ArticleFactory.createWithTag("php")
        articleB = ArticleFactory.createWithTag("javascript")
        articleC = ArticleFactory.createWithTag("php")

        response = self.client.get('/articles/?tags=php', content_type='html/text')
        self.assertIn(articleA.title, response.data)
        self.assertIn(articleC.title, response.data)
        self.assertNotIn(articleB.title, response.data)


if __name__ == '__main__':
    unittest.main()
