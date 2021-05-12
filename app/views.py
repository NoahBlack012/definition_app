from flask import Blueprint, render_template

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/")
def home():
    return "Home Page"

@views.route("/quiz/<int:topic_id>")
def quiz(topic_id):
    return f"Quiz Page {topic_id}"
