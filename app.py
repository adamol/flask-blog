from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)

db.create_all()

@app.route('/')
def welcome():
    return render_template('welcome.html')

from controllers.AuthController import AuthController
from controllers.PostsController import PostsController
from controllers.CommentsController import CommentsController

app.register_blueprint(AuthController)
app.register_blueprint(PostsController)
app.register_blueprint(CommentsController)
