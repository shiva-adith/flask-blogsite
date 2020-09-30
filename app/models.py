from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    Template for the User data model.

    ...

    Attributes
    ----------
    __tablename__ : str
        Name of the table in the database.
    username : str (limit = 30 chars)
        Unique name of the user created during Sign-up.
    email : str (limit = 120 chars)
        User's email address.
    writers_posts : Database Relationship
        Class User has a one-to-many relationship with Class BlogPost.
        For each User, the function relationship() points to BlogPost and
        loads multiple Posts written by them.
    about_me : str (limit = 250 chars)
        A short description about the user to be displayed on their profile.
    last_seen : DateTime
        Keeps track of the user's most recent active session.

    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    writers_posts = db.relationship('BlogPost', lazy='select', backref=db.backref('writer', lazy='joined'),
                                    cascade='all, delete-orphan')
    about_me = db.Column(db.String(250))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, username, email, writers_post):
    #     self.username = username
    #     self.email = email
    #     self.writers_post = writers_post

    def set_password(self, password):
        """Sets password entered by the user to the profile

        Parameters
        ----------
        password : str
            New password entered by User

        # TODO: make an entry for 'Raises' - errors encountered

        Returns
        -------
            None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the entered password against the one stored to see if they match.

        Parameters
        ----------
        password : str
            Password entered by the user.

        # TODO: make an entry for 'Raises' - errors encountered

        Returns
        -------
        Boolean
            True or False depending on whether the input matches the stored value.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # TODO/FIX : remove 'User' from the print statement
        return f"{self.username}"


@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))


# creating a template for all the posts to follow
class BlogPost(db.Model):
    """
    Template for Blog Post model

    ...

    Attributes
    ----------
    __tablename__ : str
        Name of the table in the database.
    title : str (limit = 120 chars)
        Title for the blog post.
    slug : str (limit = 60 chars)
        Shortened name for blog post.
    content : Text
        Content of the Blog Post
    date_posted : DateTime
        The date(in UTC time) on which a particular Post was created.
    writers_id : int
        A reference to the Post's author.
        Consists of a one-to-many relationship with User model. (i.e. One user, many Posts)
    category_id : int
        A reference to the category to which the Post belongs to.
        Consists of a one-to-many relationship with Category model. (i.e. One category, many Posts)
    """

    __tablename__ = "posts"
    # creating columns for each different category
    # each row reps. diff. blog posts

    # primary_key ensures that each ID s unique and can be used to identify diff. posts
    id = db.Column(db.Integer, primary_key=True)
    # nullable ensures that no title is left empty
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(60))
    content = db.Column(db.Text, nullable=False)
    # author = db.Column(db.String(30), nullable=False, default='Not Available')

    # datetime.utcnow method names are used instead of calling the methods to ensure that the
    # method is called when the posts are actually updated/posted instead of during the execution of code
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    writers_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    # date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)

    def __repr__(self):
        return f"Blog Post {str(self.id)}: {self.title}"


#  Future implementations:
#
class Category(db.Model):
    """
    Template for Category model

    ...

    Attributes
    ----------

    __tablename__ : str
        Name of the table in the database.
    name : str (limit = 30 chars)
        NMame of the Category.
    slug : str (limit = 30 chars)
        Shortened ID for a particular category.
    date_posted: DateTime
        Date(in UTC time) on which a post was created.
    category_posts : schema relationship
        Defines the one-to-many relationship with the BlogPost model.
        Backreference is provided and cascade option is delete-orphan.
    """

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # For one to many relationships:
    # relationship is usually defined in the parent class and the foreign key is placed in the child class.
    category_posts = db.relationship('BlogPost', lazy='select', backref=db.backref('category', lazy='joined'),
                                     cascade='all, delete-orphan')

    def __repr__(self):
        return f"{str(self.id)}:{self.name}"


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                     )
post_tags.__doc__ = "Manages many-to-many relationship between BlogPost and Tag models."


# class PostTags(db.Model):
#     __tablename__ = "post_tags"
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """
    Template for Tag model.

    Attributes
    ----------
    name : str (limit = 30 chars)
        Name of the tags that posts belong to.
    slug : str (limit = 30 chars)
        Shortened ID for tags.
    date_posted : DateTime
        Date(in UTC time) on which the post was created
    tag_posts : schema relationship
        Defines the many-to-many relationship between Tags and Posts
        One Tag can have many Posts, and one Post can be listed under multiple Tags.
        Backreference is provided.
    """

    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # this can be defined either here or in the Post class model
    tag_posts = db.relationship('BlogPost', secondary="post_tags", lazy='subquery', backref=db.backref('tags'))

    def __repr__(self):
        return f"{str(self.id)}:{self.name}"