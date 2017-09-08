from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'random string'
db = SQLAlchemy(app)

posts = [
    {
        'title': 'First Post',
        'body': 'Lorem ipsum, dolar sit amet'
    },
    {
        'title': 'Second Post',
        'body': 'Some more body content'
    }
]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

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

        flash('User was added')
        return redirect(url_for('posts_index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            flash('no user with that username')

            return redirect(url_for('login'))

        if not sha256_crypt.verify(request.form['password'], user.password):
            flash('login credentials did not match our records')

            return redirect(url_for('login'))

        flash('You are now logged in')

        return jsonify({
            'username': user.username,
            'email': user.email,
            'password': user.password,
        })
    else:
        return render_template('login.html')

"""
POST ROUTES
"""
@app.route('/posts')
def posts_index():
    return jsonify(posts)

@app.route('/posts/<int:id>')
def posts_show(id):
    return jsonify(posts[id])
