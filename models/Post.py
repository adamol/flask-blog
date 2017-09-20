from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

