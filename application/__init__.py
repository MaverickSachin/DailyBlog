from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    """ Construct the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app=app)

    with app.app_context():
        from application.users.views import users  # Import users blueprint
        from application.main.views import main  # Import main blueprint
        from application.posts.views import posts  # Import posts blueprint
        from application.errors.handlers import errors  # Import errors blueprint

        app.register_blueprint(users)
        app.register_blueprint(main)
        app.register_blueprint(posts)
        app.register_blueprint(errors)

        db.create_all()  # Create database tables for our data models

        return app
