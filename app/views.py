from flask import Blueprint, render_template
from .models import User, Topic, Folder
from flask_login import login_required, current_user

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/")
@login_required
def home():
    return render_template("home.html")

@views.route("/topic/<int:topic_id>")
@login_required
def topic(topic_id):
    return render_template("topic.html", topic_id=topic_id)

@views.route("/quiz/<int:topic_id>")
@login_required
def quiz(topic_id):
    return render_template("quiz.html", topic_id=topic_id)
