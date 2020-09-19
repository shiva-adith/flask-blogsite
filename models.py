from app import db
from datetime import datetime


class User(db.Model):
    """
    Template for the User data model.

    ...

    Attributes
    ----------
    __tablename__ : str
        Name of the table in the database
    username : str (limit = 30 chars)
        Unique name of the user created during Sign-up
    email : str (limit = 120 chars)
        User's email address
    writers_post : Database Relationship
        Class User has a one-to-many relationship with Class BlogPost.
        For each User, the function relationship() points to BlogPost and
        loads multiple Posts written by them.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    writers_posts = db.relationship('BlogPost', lazy='select',  backref=db.backref('writer', lazy='joined'))

    # def __init__(self, username, email, writers_post):
    #     self.username = username
    #     self.email = email
    #     self.writers_post = writers_post

    def __repr__(self):
        # TODO/FIX : remove 'User' from the print statement
        return f"User {self.username}"


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
    writers_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    # date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)

    def __repr__(self):
        return f"Blog Post {str(self.id)}:{self.title}"


#  Future implementations:
#
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # For one to many relationships:
    # relationship is usually defined in the parent class and the foreign key is placed in the child class.
    category_posts = db.relationship('BlogPost', lazy='select', backref=db.backref('category', lazy='joined'))

    def __repr__(self):
        return f"{str(self.id)}:{self.name}"


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                     )


# class PostTags(db.Model):
#     __tablename__ = "post_tags"
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # this can be defined either here or in the Post class model
    tag_posts = db.relationship('BlogPost', secondary="post_tags", lazy='subquery', backref=db.backref('tags'))

    def __repr__(self):
        return f"{str(self.id)}:{self.name}"
