from flask import Blueprint, render_template
from flask.globals import request
from flask_login import login_user, login_required, logout_user, current_user
from bcrypt import hashpw, checkpw, gensalt
from .models import User

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.quey.filter_by(username=username).first()
        if not user:
            # Flash alert
            return "Login page" # Replace with template
        
        if checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            # Login and return home page
            return "Home page"
        else:
            # Flash alert 
            pass
    return "Login page"

@auth.route("signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        user = User.quey.filter_by(username=username).first()
        if user:
            # Flask alert
            pass 
        else:
            pass
