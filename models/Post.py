from app import db

post_tag = db.Table('post_tag', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    tags = db.relationship("Tag", secondary=post_tag, backref=db.backref("posts"))

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
