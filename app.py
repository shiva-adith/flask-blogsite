from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from forms import ContactForm
from config import Config


mail = Mail()
app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail.init_app(app)

from models import BlogPost


@app.route("/") 
def index():
    return render_template('index.html')


# by default the method allowed is only GET
@app.route("/posts", methods=['GET', 'POST'])
def posts():
    # posts is a variable that we create, and the same
    # has to be referenced in the corresponding html page
    if request.method == 'POST':
        post_title = request.form['title']
        post_slug = request.form['slug']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, slug=post_slug, content=post_content, author=post_author)
        db.session.add(new_post)
        # this commits the changes to the database. Otherwise the contents 
        # will exist only in the current session and will be lost when a new sessions starts
        db.session.commit()
        return redirect('/posts')

    all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc())
    return render_template('posts.html', posts=all_posts)


@app.route("/home/users/<string:name>/posts/<int:tag>")
def hello(name, tag):
    return "Hello, " + name + " Your ID is: " + str(tag)


@app.route('/methods', methods=['GET', 'POST'])
def method():
    return "GET alone will make the page return something, eg a string (basically can't post anything!)"


@app.route('/posts/delete/<int:idx>')
def delete_post(idx):
    post = BlogPost.query.get_or_404(idx)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:idx>', methods=['GET', 'POST'])
def edit_post(idx):

    post = BlogPost.query.get_or_404(idx)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')

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
        return redirect('/posts')

    return render_template('new_post.html')


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     return render_template('contact-old.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        msg = Message(form.subject.data, recipients=['blacburn.dev@gmail.com'])
        msg.body = f"""From: {form.name.data} <{form.email.data}>
                                        {form.message.data}"""
        mail.send(msg)
        return render_template('contact.html', success=True)

    # if request.method == 'POST':
    #     if not form.validate():
    #         return render_template('contact.html', form=form)
    #     else:
    #         msg = Message(form.subject.data, recipients=['blacburn.dev@gmail.com'])
    #         msg.body = f"""From: {form.name.data} <{form.email.data}>
    #                              {form.message.data}"""
    #
    #         # msg.body = "Hello"
    #         mail.send(msg)
    #         # return "Form posted"
    #         return render_template('contact.html', success=True)

    return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
