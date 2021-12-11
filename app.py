import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
# from werkzeug.exceptions import abort
# from flask_mongoengine import MongoEngine
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from bson import json_util
from bson.json_util import loads, dumps
import os
from datetime import datetime
from functools import wraps


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}
# db = MongoEngine()
# db.init_app(app)

app.config["MONGODB_URI"] = 'mongodb://' + 'root' + ':' + 'password' + '@' + 'srv-captain--mongo' + ':27017/' + 'amphibia'
# client = MongoClient()
# db = mongo.db

host = os.environ.get('MONGODB_URI', 'mongodb://srv-captain--mongo:27017/amphibia')
client = MongoClient(host=f'{host}?retryWrites=false', connect=False)
db = client.get_default_database()
users = db.users
posts = db.posts
comments = db.comments

def login_required(f):
    """
    Require login to access a page.

    Adapted from:
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------OLD DB?---------------------------
# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn
#
# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                         (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'go ahead and hack this'

# ---------------------------LOGIN/OUT---------------------------
@app.route('/login')
def login():
    """Login form."""
    if 'user' in session:
        current_user = session['user']
        return render_template('users/logged_in.html',
                               current_user=current_user)
    # print("h")
    return render_template('users/login.html')


@app.route('/login/submit', methods=['POST'])
def login_submit():
    """Login submit."""
    current_user = None
    if 'user' in session:
        current_user = session['user']

    user = users.find_one({'username': request.form.get('username')})

    if user is None:
        return redirect(url_for('login'))
    if user['password'] != request.form.get('password'):
        return redirect(url_for('login'))

    data = {
        'username': request.form.get('username'),
        'user_id': str(user['_id'])
    }

    session['user'] = json.loads(json_util.dumps(data))

    current_user = session['user']
    return redirect(url_for('users_show', user_id=data['user_id']))


@app.route('/logout')
def logout():
    """Remove user from session."""
    session.clear()
    return redirect(url_for('index'))


# ---------------------------USERS---------------------------
@app.route('/users/new')
def users_new():
    """Return a user creation page."""
    if 'user' in session:
        current_user = session['user']
        return render_template('users/logged_in.html',
                               current_user=current_user)
    return render_template('users/new_user.html', user={}, title='New User')


@app.route('/users/directory')
def users_directory():
    """Return a directory of users."""
    current_user = None
    if 'user' in session:
        current_user = session['user']

    return render_template('users/users_directory.html', users=users.find(),
                           current_user=current_user)


@app.route('/users', methods=['POST'])
def users_submit():
    """Submit a new user."""
    if 'user' in session:
        current_user = session['user']
        return render_template('users/logged_in.html',
                               current_user=current_user)

    if users.find_one({'username': request.form.get('username')}) is not None:
        return redirect(url_for('users_new'))

    user = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'bio': request.form.get('content'),
        'created_at': datetime.now()
    }

    user_id = users.insert_one(user).inserted_id

    data = {
        'username': request.form.get('username'),
        'user_id': str(user_id)
    }

    session['user'] = json.loads(json_util.dumps(data))
    return redirect(url_for('users_show', user_id=user_id))

@app.route('/users/<user_id>')
def users_show(user_id):
    """Show a single user page."""
    current_user = None
    if 'user' in session:
        current_user = session['user']

    user = users.find_one({'_id': ObjectId(user_id)})

    user_posts = posts.find({'user_id': ObjectId(user_id)})
    return render_template('users/users_show.html', user=user,
                           posts=user_posts,
                           current_user=current_user)


@app.route('/')
def index():
    current_user = None
    if 'user' in session:
        current_user = session['user']
    return render_template('index.html', posts=posts.find(),
                            current_user=current_user)

@app.route('/<post_id>')
def post(post_id):
    current_user = None
    if 'user' in session:
        current_user = session['user']

    post = posts.find_one({'_id': ObjectId(post_id)})
    post_comments = comments.find({'post_id': ObjectId(post_id)})
    post_author = users.find({'_id': post['user_id']})

    updated_views = {
        'views': post['views'] + 1
    }
    posts.update_one(
        {'_id': ObjectId(post_id)},
        {'$set': updated_views})

    return render_template('post.html', post=post,
                           comments=post_comments, user=post_author,
                           current_user=current_user)
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    current_user = session['user']

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            post = {
                'title': title,
                'description': content,
                'views': 0,
                'created_at': datetime.now(),
                'author': current_user['username'],
                'user_id': ObjectId(current_user['user_id'])
    }
            post_id = posts.insert_one(post).inserted_id
            return redirect(url_for('post', post_id=post_id))

    return render_template('create.html')

@app.route('/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    current_user = session['user']
    post = posts.find_one({'_id': ObjectId(id)})

    if ObjectId(current_user['user_id']) != post['user_id']:
        return render_template('wrong_user.html', current_user=current_user)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            updated_post = {
                'title': request.form.get('title'),
                'description': request.form.get('content')
            }
            posts.update_one(
                {'_id': ObjectId(id)},
                {'$set': updated_post})
            return redirect(url_for('post', post_id=id))

    return render_template('edit.html', post=post)

@app.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    current_user = session['user']
    post = posts.find_one({'_id': ObjectId(id)})

    if ObjectId(current_user['user_id']) != post['user_id']:
        return render_template('wrong_user.html', current_user=current_user)

    posts.delete_one({'_id': ObjectId(id)})

    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# ---------------------------COMMENTS---------------------------
@app.route('/posts/comments', methods=['POST'])
@login_required
def comments_new():
    """Submit a new comment."""
    current_user = session['user']
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'post_id': ObjectId(request.form.get('post_id')),
        'author': current_user['username'],
        'user_id': ObjectId(current_user['user_id'])
    }
    comments.insert_one(comment)
    return redirect(url_for('post',
                            post_id=request.form.get('post_id')))


@app.route('/comments/<comment_id>', methods=['POST'])
@login_required
def comments_delete(comment_id):
    """Delete a comment."""
    current_user = session['user']
    comment = comments.find_one({'_id': ObjectId(comment_id)})

    if ObjectId(current_user['user_id']) != comment['user_id']:
        return render_template('wrong_user.html', current_user=current_user)

    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('post',
                            post_id=comment.get('post_id')))
