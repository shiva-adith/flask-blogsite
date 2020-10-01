from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.urls import url_parse
from app import app, db, mail
from app.forms import LoginForm, ContactForm, RegistrationForm
from app.models import User, BlogPost
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/user/<username>')
@login_required
def users(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()
    post = [
        {'author': user, 'content': 'Test post #1'},
        {'author': user, 'content': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=post)


# by default the method allowed is only GET
@app.route("/posts", methods=['GET', 'POST'])
# @login_required
def posts():
    # posts is a variable that we create, and the same
    # has to be referenced in the corresponding html page
    # if request.method == 'POST':
    #     post_title = request.form['title']
    #     post_slug = request.form['slug']
    #     post_content = request.form['content']
    #     post_author = request.form['author']
    #     new_post = BlogPost(title=post_title, slug=post_slug, content=post_content, author=post_author)
    #     db.session.add(new_post)
    #     # this commits the changes to the database. Otherwise the contents
    #     # will exist only in the current session and will be lost when a new sessions starts
    #     db.session.commit()
    #     return redirect('/posts')

    # all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc())
    all_posts = db.session.query(BlogPost).order_by(BlogPost.date_posted.desc())
    return render_template('posts.html', posts=all_posts)


@app.route("/home/users/<string:name>/posts/<int:tag>")
def hello(name, tag):
    return "Hello, " + name + " Your ID is: " + str(tag)


@app.route('/methods', methods=['GET', 'POST'])
def method():
    return "GET alone will make the page return something, eg a string (basically can't post anything!)"


@app.route('/posts/delete/<int:idx>')
def delete_post(idx):
    # post = BlogPost.query.get_or_404(idx)
    post = db.session.query(BlogPost).get_or_404(idx)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:idx>', methods=['GET', 'POST'])
def edit_post(idx):

    # post = BlogPost.query.get_or_404(idx)
    post = db.session.query(BlogPost).get_or_404(idx)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('edit.html', posts=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, author=post_author, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('new_post.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Great job! You're now part of the network!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
        

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        msg = Message(form.subject.data, recipients=['blacburn.dev@gmail.com'])
        msg.body = f"""From: {form.name.data} <{form.email.data}>
                                        {form.message.data}"""
        mail.send(msg)
        return render_template('contact.html', success=True)

    return render_template('contact.html', form=form)
