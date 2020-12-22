import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #secret keys
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = 'secret-salt'

    DATABASE_URL = 'postgres://gmgskvzrhawssf:529c332f2de37b3b2e968a914ae398bb2b9a744eceb6ed5ad3da41a8d49ef058@ec2-54-237-135-248.compute-1.amazonaws.com:5432/dmnha41oe8n1h'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #mail
    MAIL_SUBJECT = 'Confirm Your Meditation Account'