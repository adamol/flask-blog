from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)

db.create_all()

@app.route('/')
def welcome():
    return render_template('welcome.html')

from controllers.AuthController import AuthController
from controllers.ArticlesController import ArticlesController
from controllers.CommentsController import CommentsController
from controllers.ArticleLikesController import ArticleLikesController

app.register_blueprint(AuthController)
app.register_blueprint(ArticlesController)
app.register_blueprint(CommentsController)
app.register_blueprint(ArticleLikesController)
