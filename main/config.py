import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #secret keys
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = 'secret-salt'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #mail
    MAIL_SUBJECT = 'Confirm Your Meditation Account'