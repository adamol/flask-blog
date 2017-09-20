from app import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(250))

    def __init__(self, post_id, user_id, body):
        self.post_id = post_id
        self.user_id = user_id
        self.body = body
