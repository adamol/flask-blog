from app import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(250))

    user = db.relationship('User')
    article = db.relationship('Article')

    def __init__(self, article_id, user_id, body):
        self.article_id = article_id
        self.user_id = user_id
        self.body = body
