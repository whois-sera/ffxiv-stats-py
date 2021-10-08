import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))  # Load .env. while .flaskenv is autoloaded

class Config(object):
    """Config class that is passed to Flask to map configuration"""

    """
        Values are mapped from .env and .flaskenv files with os.environ.get("CONST")
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False