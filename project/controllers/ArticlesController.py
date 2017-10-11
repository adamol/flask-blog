from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from project.models import Article, Tag, Comment, User
from app import db

from flask import jsonify

ArticlesController = Blueprint('articles', __name__, url_prefix='/articles', template_folder='../templates')

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

        if not request.form['tags']:
            flash('You must enter a tag when submitting a new article.')

            return redirect(url_for('articles.index'))


        article = Article(request.form['title'], request.form['body'], current_user.id)

        if ',' in request.form['tags']:
            tags = request.form['tags'].split(',')
        else:
            tags = [request.form['tags']]

        article.tags.extend([Tag(tag) for tag in tags])

        db.session.add(article)
        db.session.commit()

        return redirect(url_for('articles.index'))
    else:
        if request.args.get('tags'):
            tags = request.args.get('tags')
            if ',' in tags:
                tags = tags.split(',')
            else:
                tags = [tags]

            q = db.session.query(Article)
            for tag in tags:
                q = q.filter(Article.tags.any(name=tag))

            articles = q.all()
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

