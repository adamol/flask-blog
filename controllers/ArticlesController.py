from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from models.Article import Article
from models.Article import Tag
from models.Comment import Comment
from models.User import User
from app import db

from flask import jsonify

ArticlesController = Blueprint('articles', __name__, url_prefix='/articles')

@ArticlesController.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_user = User.query.filter_by(username=session['username']).first()

        if not current_user.is_admin():
            flash('You must be an admin in order to add a article.')

            return redirect(url_for('articles.index'))

        if not request.form['title']:
            flash('You must enter a article title when submitting a new article.')

            return redirect(url_for('articles.index'))

        if not request.form['body']:
            flash('You must enter a article body when submitting a new article.')

            return redirect(url_for('articles.index'))

        if not request.form['tag']:
            flash('You must enter a tag when submitting a new article.')

            return redirect(url_for('articles.index'))


        article = Article(request.form['title'], request.form['body'], current_user.id)
        tag  = Tag(request.form['tag'])
        article.tags.append(tag)

        db.session.add(article)
        db.session.add(tag)
        db.session.commit()

        return redirect(url_for('articles.index'))
    else:
        if request.args.get('tags'):
            tag = request.args.get('tags')
            articles = Article.query.filter(Article.tags.any(name=tag)).all()
        else:
            articles = Article.query.all()

        return render_template('articles_index.html', articles=articles)

@ArticlesController.route('/<int:id>')
def show(id):
    article = Article.query.filter_by(id=id).first()
    article.user = User.query.filter_by(id=article.user_id).first()

    comments = Comment.query.filter_by(article_id=article.id).all()
    for comment in comments:
        comment.user = User.query.filter_by(id=comment.user_id).first()

    return render_template('articles_show.html', article=article, comments=comments)

