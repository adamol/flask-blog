from flask import Blueprint, redirect, url_for, session, flash
from project.models import Article, Like, User
from app import db

ArticleLikesController = Blueprint('article_likes', __name__)

@ArticleLikesController.route('/articles/<int:article_id>/likes', methods=['POST'])
def store(article_id):
    if 'username' in session.keys():
        current_user = User.query.filter_by(username=session['username']).first()
    else:
        flash('Guests cannot submit likes.')

        return redirect(url_for('articles.show', id=article_id))

    article = Article.query.filter_by(id=article_id).first()

    foundLike = Like.query.filter_by(
            user_id=current_user.id, article_id=article.id
    ).first()

    if foundLike:
        db.session.delete(foundLike)
        db.session.commit()

        return redirect(url_for('articles.show', id=article_id))
    else:
        db.session.add(Like(current_user.id, article.id))

        return redirect(url_for('articles.show', id=article_id))
