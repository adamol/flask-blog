from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'random string'
db = SQLAlchemy(app)

"""
MODELS
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body

db.create_all()

@app.route('/')
def welcome():
    return render_template('welcome.html')

"""
AUTH ROUTES
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return redirect(url_for('register'))

        if request.form['password'] == '' or request.form['username'] == '' or request.form['email'] == '':
            return redirect(url_for('register'))

        user = User(
            request.form['username'],
            request.form['email'],
            sha256_crypt.encrypt(request.form['password'])
        )

        db.session.add(user)
        db.session.commit()

        session['username'] = request.form['username']

        flash('User was added')

        return redirect(url_for('posts_index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            flash('No user with that username.')

            return redirect(url_for('login'))

        if not sha256_crypt.verify(request.form['password'], user.password):
            flash('login credentials did not match our records')

            return redirect(url_for('login'))

        session['username'] = request.form['username']

        flash('You are now logged in')

        return redirect(url_for('posts_index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)

    flash('You are now logged out.')

    return redirect(url_for('login'))

"""
POST ROUTES
"""
@app.route('/posts', methods=['GET', 'POST'])
def posts_index():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['body']:
            flash('You must enter both a title and a body when submitting a new post')

            return redirect(url_form('posts_index'))

        post = Post(request.form['title'], request.form['body'])

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts_index'))
    else:
        posts = Post.query.all()

        return render_template('posts_index.html', posts=posts)

@app.route('/posts/<int:id>')
def posts_show(id):
    post = Post.query.filter_by(id=id).first()

    return render_template('posts_show.html', post=post)
