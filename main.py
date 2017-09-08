from flask import Flask, jsonify, render_template, request
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.debug = True

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

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        encrypted_pass = sha256_crypt.encrypt(request.form['password'])

        return jsonify({
            'username': request.form['username'],
            'email': request.form['email'],
            'password': encrypted_pass,
            'confirm_password': request.form['confirm_password'],
            'check_pass': sha256_crypt.verify('secret', encrypted_pass)
        })
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#

@app.route('/posts')
def postsIndex():
    return jsonify(posts)

@app.route('/posts/<int:id>')
def postsShow(id):
    return jsonify(posts[id])
