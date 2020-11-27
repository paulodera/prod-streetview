import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ['DEBUG']

SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']
