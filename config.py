import os
from dotenv import load_dotenv

BASE_DIR = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(BASE_DIR)

DEBUG = os.getenv('DEBUG')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')
SECRET_KEY = os.getenv('SECRET')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')
