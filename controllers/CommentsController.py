from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from models.Comment import Comment
from models.User import User
from app import db

CommentsController = Blueprint('comments', __name__)

@CommentsController.route('/posts/<int:post_id>/comments', methods=['POST'])
def store(post_id):
    if not request.form['body']:
        flash('You must enter a comment body.')

        return redirect(url_for('posts.show', id=post_id))

    if 'username' in session.keys():
        current_user = User.query.filter_by(username=session['username']).first()
    else:
        flash('You must be logged in to post a comment.')

        return redirect(url_for('posts.show', id=post_id))

    comment = Comment(post_id, current_user.id, request.form['body'])

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('posts.show', id=post_id))

