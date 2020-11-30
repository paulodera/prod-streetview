import os
from dotenv import load_dotenv

load_dotenv()
postgres://ttxooertajrmek:6e39f1006003c3fc3a3c4bdabf361a723471f9b455893dc473ca639330a5afff@ec2-52-203-182-92.compute-1.amazonaws.com:5432/d1ge2urdv81f7t

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ['DEBUG']

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']
