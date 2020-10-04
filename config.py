from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# FLASK_APP = environ.get('FLASK_APP')
# SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SECRET_KEY = environ.get('SECRET_KEY')
#
# # Email server
# MAIL_SERVER = "smtp.gmail.com"
# MAIL_PORT = 587
# # MAIL_USE_TLS = True
# MAIL_USE_SSL = True
# MAIL_USERNAME = environ.get('MAIL_USERNAME')
# MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
# MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
#
# # Admin list
# ADMINS = environ.get('ADMINS')
# # python -m smtpd -n -c DebuggingServer localhost:8025


class Config:
    """Set Flask config variables. """
    FLASK_APP = environ.get('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')

    # Email server
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

    # Admin list
    ADMINS = environ.get('ADMINS')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
