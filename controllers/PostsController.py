from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from app.models.Post import Post
from app.models.Comment import Comment
from app.models.User import User
from app import db

from flask import jsonify

PostsController = Blueprint('posts', __name__, url_prefix='/posts')

@PostsController.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['body']:
            flash('You must enter both a title and a body when submitting a new post')

            return redirect(url_for('posts.index'))

        current_user = User.query.filter_by(username=session['username']).first()
        post = Post(request.form['title'], request.form['body'], current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.index'))
    else:
        posts = Post.query.all()

        return render_template('posts_index.html', posts=posts)

@PostsController.route('/<int:id>')
def show(id):
    post = Post.query.filter_by(id=id).first()
    post.user = User.query.filter_by(id=post.user_id).first()

    comments = Comment.query.filter_by(post_id=post.id).all()
    for comment in comments:
        comment.user = User.query.filter_by(id=comment.user_id).first()

    return render_template('posts_show.html', post=post, comments=comments)

