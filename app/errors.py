from flask import render_template
from app import app, db

# The error pages are only displayed in the production env. ie. when Debug mode if off.


@app.errorhandler(404)
def not_found_error(error):
    # error view functions require an extra return value(404/500)
    # to be passed since the default val. is 200 which indicates
    # a successful response. (200 is passed when nothing is specified)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # to ensure that errors don't interfere with the DB accesses,
    # (eg. invalid usernames being saved) a rollback is performed.
    db.session.rollback()
    return render_template('500.html'), 500
