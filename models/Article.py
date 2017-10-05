from app import db

article_tag = db.Table('article_tag', db.Model.metadata,
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(40))
    body = db.Column(db.String(250))

    user = db.relationship('User')

    tags = db.relationship("Tag", secondary=article_tag, backref=db.backref("articles"))

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(40), index=True)

    def __init__(self, name):
        self.name = name
