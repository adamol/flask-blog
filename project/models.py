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
    likes = db.relationship("Like")
    # comments ?

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

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id, article_id):
        self.user_id = user_id
        self.article_id = article_id
        # self.likeable_id = likeable_id
        # self.likeable_type = likeable_type

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

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

    articles = db.relationship("Article", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_admin(self):
        return self.username == "admin"

