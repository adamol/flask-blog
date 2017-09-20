from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test6.db'
app.config['SECRET_KEY'] = 'random string'
db = SQLAlchemy(app)

from app.models.User import User
from app.models.Post import Post
from app.models.Comment import Comment
db.create_all()

@app.route('/')
def welcome():
    return render_template('welcome.html')

from app.controllers.AuthController import AuthController
from app.controllers.PostsController import PostsController
from app.controllers.CommentsController import CommentsController

app.register_blueprint(AuthController)
app.register_blueprint(PostsController)
app.register_blueprint(CommentsController)
