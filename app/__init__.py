from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URI"]
    db.init_app(app)

    db.create_all(app=app)

    from .views import views
    from . import models


    app.register_blueprint(views, url_prefix="/")

    return app