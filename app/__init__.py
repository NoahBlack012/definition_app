from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_manager
from flask_session import Session
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["SECRET_KEY"]
    #app.config["SESSION_PERMANENT"] = True
    #app.config["SESSION_TYPE"] = "filesystem"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URI"]
    db.init_app(app)
    #Session(app)
    #app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    #CORS(app)

    from .views import views
    from .auth import auth
    from .models import User, Folder, Topic

    # Register Blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app