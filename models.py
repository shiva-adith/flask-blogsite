from app import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('BlogPost', backref='category')

    def __repr__(self):
        return f"{str(self.id)}:{self.author}"


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )


# creating a template for all the posts to follow
class BlogPost(db.Model):
    __tablename__ = "posts"
    # creating columns for each different category
    # each row reps. diff. blog posts

    # primary_key ensures that each ID s unique and can be used to identify diff. posts
    id = db.Column(db.Integer, primary_key=True)
    # nullable ensures that no title is left empty
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Not Available')
    # datetime.utcnow method names are used instead of calling the methods to ensure that the
    # method is called when the posts are actually updated/posted instead of during the execution of code
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f"Blog Post {str(self.id)}:{self.title}"


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # this can be defined either here or in the Post class model
    posts = db.relationship('BlogPost', secondary=post_tags, backref='tags')

    def __repr__(self):
        return f"{str(self.id)}:{self.author}"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User {self.username}"
