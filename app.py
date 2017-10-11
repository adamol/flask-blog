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

from project.controllers.AuthController import AuthController
from project.controllers.ArticlesController import ArticlesController
from project.controllers.CommentsController import CommentsController
from project.controllers.ArticleLikesController import ArticleLikesController

app.register_blueprint(AuthController)
app.register_blueprint(ArticlesController)
app.register_blueprint(CommentsController)
app.register_blueprint(ArticleLikesController)
