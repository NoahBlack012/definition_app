from flask import Blueprint, render_template, request, redirect, url_for
from flask.globals import session
from flask.helpers import flash
from .models import User, Topic, Folder
from flask_login import login_required, current_user
from . import db

from .create_quiz import create_quiz

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")

def check_user(userid, folderid=None, topic_id=None):
    if folderid:
        folder = Folder.query.filter_by(id=folderid).first()
        if not folder or folder.userid != userid:
            return False
    else:
        topic = Topic.query.filter_by(id=topic_id).first()
        folder = Folder.query.filter_by(id=topic.folderid).first()
        if not topic or not folder or folder.userid != userid:
            return False 
    return True

def verify_topic(userid, topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    folder = Folder.query.filter_by(id=topic.folderid).first()
    if not topic or not folder or folder.userid != userid:
        return False 
    return True

@views.route("/")
@login_required
def home():
    folders = Folder.query.filter_by(userid=current_user.id).all()
    return render_template("home.html", folders=folders, username=current_user.username)

@views.route("/folder/<int:folder_id>")
@login_required
def folder(folder_id):
    folder = Folder.query.filter_by(id=folder_id).first()
    return render_template("folder.html", folder=folder, username=current_user.username)

@views.route("/topic/<int:topic_id>")
@login_required
def topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    if not verify_topic(current_user.id, topic_id):
        return redirect(url_for("views.home"))
    return render_template("topic.html", topic=topic, username=current_user.username)

@views.route("/quiz/<int:topic_id>", methods=["GET", "POST"])
@login_required
def quiz(topic_id):
    question_number = int(request.args.get("question_number"))
    if question_number == 0:
        topic = Topic.query.filter_by(id=topic_id).first()
        if not verify_topic(current_user.id, topic_id):
            return redirect(url_for("views.home"))
        
        data = topic.data
        if len(data) < 4:
            flash("To generate a quiz, you must add at least four definitions to the topic", "error")
            return redirect(url_for("views.topic", topic_id=topic_id))
        quiz = create_quiz(data, len(data))
        session["question_number"] = 0
        session["final_question"] = len(quiz) - 1
        session["quiz"] = quiz
        last_question = False
    elif question_number == session["final_question"]:
        last_question = True 
    else:
        last_question = False
    
    session["question_number"] = question_number
    return render_template("quiz.html", 
            topic_id=topic_id, 
            username=current_user.username, 
            question=session["quiz"][question_number],
            question_number=question_number+1,
            last_question=last_question
            )


@views.route("/add_folder", methods=["POST"])
@login_required
def add_folder():
    name = request.form.get("name")
    db_folder = Folder.query.filter_by(name=name, userid=current_user.id).first()
    if db_folder:
        flash("Sorry, that folder name has already been used", category="error")
        return redirect(url_for("views.home"))

    new_folder = Folder(userid=current_user.id, name=name)
    db.session.add(new_folder)
    db.session.commit()
    flash("Folder created", category="success")
    return redirect(url_for("views.home"))

@views.route("/add_topic/<int:folder_id>", methods=["POST"])
@login_required
def add_topic(folder_id):
    title = request.form.get("title")
    if not check_user(current_user.id, folderid=folder_id):
        return redirect(url_for("auth.logout"))

    db_topic = Topic.query.filter_by(title=title, folderid=folder_id).first()
    if db_topic:
        flash("Sorry, that topic name has already been used", category="error")
        return redirect(url_for("views.folder", folderid=folder_id))


    new_topic = Topic(title=title, folderid=folder_id, data={})
    db.session.add(new_topic)
    db.session.commit()
    flash("Topic created", category="success")
    return redirect(url_for("views.folder", folder_id=folder_id))

@views.route("/add_data/<int:topic_id>", methods=["POST"])
@login_required
def add_data(topic_id):
    key = request.form.get("key")
    value = request.form.get("value")

    topic = Topic.query.filter_by(id=topic_id).first()
    if not verify_topic(current_user.id, topic_id):
        return redirect(url_for("auth.logout"))

    if key in topic.data:
        flash("That concept is already defined in this topic", "error")
        return redirect(url_for("views.topic", topic_id=topic_id))

    # Update database
    data = topic.data
    data[key] = value 
    Topic.query.filter_by(id=topic_id).update(dict(data=data))
    db.session.commit()

    return redirect(url_for("views.topic", topic_id=topic_id))

@views.route("/edit_def", methods=["POST"])
@login_required
def edit_def():
    old_key = request.args.get("def")
    topic_id = request.args.get("topic_id")
    new_key = request.form.get("new_key")
    new_value = request.form.get("new_value")

    topic = Topic.query.filter_by(id=topic_id).first()
    if not verify_topic(current_user.id, topic_id):
        return redirect(url_for("auth.logout"))

    data = topic.data 
    data.pop(old_key, None)

    data[new_key] = new_value
    Topic.query.filter_by(id=topic_id).update(dict(data=data))
    db.session.commit()

    return redirect(url_for("views.topic", topic_id=topic_id))

@views.route("/delete_def", methods=["POST"])
def delete_def():
    topic_id = request.args.get("topic_id")
    definition = request.args.get("def")

    if not verify_topic(current_user.id, topic_id):
        return redirect(url_for("auth.logout"))

    topic = Topic.query.filter_by(id=topic_id).first()
    data = topic.data
    data.pop(definition)
    Topic.query.filter_by(id=topic_id).update(dict(data=data))
    db.session.commit()

    return redirect(url_for("views.topic", topic_id=topic_id))






    
    