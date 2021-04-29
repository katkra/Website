import os
from dotenv import load_dotenv
import gunicorn


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    MAIL_SERVER = 'smtp.gmail.com'#os.environ.get('MAIL_SERVER')
    MAIL_PORT =465#int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS =False #os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL=True
    MAIL_USERNAME = 'katkra1994@googlemail.com'#os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['katkra1994@googlemail.com']
    LANGUAGES = ['en', 'da','dk']
    ELASTICSEARCH_URL = 'http://localhost:9200'#os.environ.get('ELASTICSEARCH_URL')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    #MAIL_SERVER=localhost
    #MAIL_PORT=25
    #DATABASE_URL=mysql+pymysql://web:giraffenpo@localhost:3306/web
   