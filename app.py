from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from forms import ContactForm
from datetime import datetime

mail = Mail()
app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
mail.init_app(app)


# creating a template for all the posts to follow
class BlogPost(db.Model):
    __tablename__ = "posts"
    # creating columns for each different category
    # each row reps. diff. blog posts

    # primary_key ensures that each ID s unique and can be used to identify diff. posts
    id = db.Column(db.Integer, primary_key=True)
    # nullable ensures that no title is left empty
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Not Available')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Blog Post " + str(self.id)


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
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        # this commits the changes to the database. Otherwise the contents 
        # will exist only in the current session and will be lost when a new sessions starts
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted)
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
    else:
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
    else:
        return render_template('new_post.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@app.route('/cntct', methods=['GET', 'POST'])
def cntctpg():
    form = ContactForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('cntct.html', form=form)
        else:
            msg = Message(form.subject.data, sender='blacburn.dev@gmail.com', recipients=['shivaadith@gmail.com', '2020mt93134@wilp.bits-pilani.ac.in'])
            msg.body = f"""From: {form.name.data} <{form.email.data}>
                           {form.message.data}"""
            msg.send(msg)
            return render_template('cntct.html', success=True)

    elif request.method == 'GET':
        return render_template('cntct.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
