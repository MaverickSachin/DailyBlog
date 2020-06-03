from os import path
from dotenv import load_dotenv
from decouple import config

base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, '.env'))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    SECRET_KEY = config('SECRET_KEY')
    FLASK_ENV = config('FLASK_ENV')
    FLASK_APP = config('FLASK_APP')
    FLASK_DEBUG = config('FLASK_DEBUG')

    # Database
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
