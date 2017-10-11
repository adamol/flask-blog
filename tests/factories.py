from models.Article import Article
from models.Article import Tag
from models.User import User
from app import db
from passlib.hash import sha256_crypt
from random import randint
import time

class ArticleFactory:

    @staticmethod
    def create():
        user  = UserFactory.getAdmin()
        title = "TITLE:" + str(time.time()*100) + str(randint(1,1000000))
        body  = "TEST CONTENT"

        article = Article(title, body, user.id)
        db.session.add(article)

        return article

    @staticmethod
    def createWithTag(tagName):
        article = ArticleFactory.create()
        tag = Tag.query.filter_by(name=tagName).first()

        article.tags.append(tag)

        db.session.add(article)

        return article

class UserFactory:

    @staticmethod
    def getAdmin():
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin  = User("admin","admin@example.com", sha256_crypt.hash("admin"))
            db.session.add(admin)

        return admin
