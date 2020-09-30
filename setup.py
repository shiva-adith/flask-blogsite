from app import app, db
from app.models import User, BlogPost, Category, Tag


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': BlogPost, 'Cat':Category, 'Tag': Tag}


if __name__ == "__main__":
    app.run(debug=True)
