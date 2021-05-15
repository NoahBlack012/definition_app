from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    folders = db.relationship("Folder")

    def __repr__(self) -> str:
        return f"{self.username}, {self.password}"

class Folder(db.Model):
    __tablename__ = "folders"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String, nullable=False)
    subtopics = db.relationship("Topic")

    def __repr__(self) -> str:
        return f"{self.name}, {self.subtopics}"

class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    folderid = db.Column(db.Integer, db.ForeignKey("folders.id"))
    title = db.Column(db.String, nullable=False)
    data = db.Column(db.JSON, nullable=True)

    def __repr__(self) -> str:
        return f"{self.title}, {self.data}"