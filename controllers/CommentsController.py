from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from project.models import Comment, User
from app import db

CommentsController = Blueprint('comments', __name__)

@CommentsController.route('/articles/<int:article_id>/comments', methods=['POST'])
def store(article_id):
    if not request.form['body']:
        flash('You must enter a comment body.')

        return redirect(url_for('articles.show', id=article_id))

    if 'username' in session.keys():
        current_user = User.query.filter_by(username=session['username']).first()
    else:
        flash('You must be logged in to article a comment.')

        return redirect(url_for('articles.show', id=article_id))

    comment = Comment(article_id, current_user.id, request.form['body'])

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('articles.show', id=article_id))

