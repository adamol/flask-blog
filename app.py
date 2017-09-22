from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)

db.create_all()

from controllers.AuthController import AuthController
from controllers.PostsController import PostsController
from controllers.CommentsController import CommentsController

app.register_blueprint(AuthController)
app.register_blueprint(PostsController)
app.register_blueprint(CommentsController)
