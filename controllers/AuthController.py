from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from passlib.hash import sha256_crypt
from models.User import User
from app import db

AuthController = Blueprint('auth', __name__, url_prefix='/auth')

@AuthController.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return redirect(url_for('auth.register'))

        if request.form['password'] == '' or request.form['username'] == '' or request.form['email'] == '':
            return redirect(url_for('auth.register'))

        user = User(
            request.form['username'],
            request.form['email'],
            sha256_crypt.hash(request.form['password'])
        )

        db.session.add(user)
        db.session.commit()

        session['username'] = request.form['username']

        if user.is_admin():
            session['isAdmin'] = True
        else:
            session['isAdmin'] = False

        flash('User was added')

        return redirect(url_for('articles.index'))
    else:
        return render_template('register.html')

@AuthController.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            flash('No user with that username.')

            return redirect(url_for('auth.login'))

        if not sha256_crypt.verify(request.form['password'], user.password):
            flash('Password did not match our records.')

            return redirect(url_for('auth.login'))

        session['username'] = request.form['username']

        if user.is_admin():
            session['isAdmin'] = True
        else:
            session['isAdmin'] = False

        flash('You are now logged in as ' + session['username'])

        return redirect(url_for('articles.index'))
    else:
        return render_template('login.html')

@AuthController.route('/logout')
def logout():
    session.pop('username', None)

    flash('You were logged out.')

    return redirect(url_for('auth.login'))

