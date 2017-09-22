from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from models.Comment import Comment
from models.User import User
from app import db

CommentsController = Blueprint('comments', __name__)

@CommentsController.route('/posts/<int:post_id>/comments', methods=['POST'])
def store(post_id):
    if not request.form['body']:
        return redirect(url_for('posts.show', id=post_id))

    current_user = User.query.filter_by(username=session['username']).first()
    comment = Comment(post_id, current_user.id, request.form['body'])

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('posts.show', id=post_id))

