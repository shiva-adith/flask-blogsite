from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

mail = Mail()
app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
mail.init_app(app)

from app import routes, models, errors

if not app.debug:
    # Email logging: (logLevel = ERROR)
    # logs major errors and sends an email to the admin.
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                                   toaddrs=app.config['ADMINS'], subject='Blog Failure',
                                   credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # File Logging: (logLevel = INFO)
    # logs only exceptions raised by python that aren't major errors.
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/blogsite.log', maxBytes=10240, backupCount=10)
    # the logging format in the file includes the timestamp, logging level, the message, source file and line number
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Blogsite startup')
