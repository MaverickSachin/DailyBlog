from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


""" Construct the core application"""
app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')

db = SQLAlchemy()
db.init_app(app=app)

bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

with app.app_context():
    from . import views  # Import routes
    db.create_all()  # Create database tables for our data models
