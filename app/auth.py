from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from flask_login import login_user, login_required, logout_user, current_user
import bcrypt
from .models import User
from string import punctuation
from . import db

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

def check_pw_conditions(pw):
    symbol = False
    capital = False 
    number = False
    symbols = list(punctuation)
    capitals = [chr(i) for i in range(65, 91)]
    numbers = [str(i) for i in range(0, 10)]
    for i in pw:
        if i in symbols:
            symbol = True 
        if i in capitals:
            capital = True 
        if i in numbers:
            number = True 
        
        if symbol and capital and number:
            return True 
    return False

def valid_email(email):
    if "@" not in email:
        return False 
    email = email.split("@")
    if len(email) != 2:
        return False
    
    if "." not in email[1]:
        return False 
    
    if not email[0] or not email[1]:
        return False 

    after_at = email[1].split(".")
    if not after_at[0] or not after_at[1]:
        return False
    return True

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            # Flash alert - user does not exist
            flash("The username or password you entered is incorrect", "error")
            return render_template("login.html")
        
        db_password = db_user.password
        if bcrypt.checkpw(password.encode("utf-8"), db_password.encode("utf-8")):
            flash("Login successful", "success")
            # Login and return home page
            login_user(db_user, remember=True)
            return redirect(url_for("views.home"))
        else:
            # Flash alert - incorrect password
            flash("The username or password you entered is incorrect", "error")
    elif not current_user.is_authenticated:
        return render_template("login.html")
    return redirect(url_for("views.home"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not email or not username or not password or not confirm_password:
            flash("Please fill out all required fields", "error")
            return render_template("signup.html")
        if " " in email or " " in username:
            flash("Please do not include spaces in the username or email", "error")
            return render_template("signup.html")
        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        if user:
            # Flash alert - name already take
            flash("That username is already taken", "error")
        elif email_user:
            flash("Sorry, that email is already in use", "error")
        else:
            if password != confirm_password:
                # Flash alert - passwords do not match
                flash("The passwords entered do not match", "error")
            elif len(password) < 7:
                # Flash alert - password must be 7 characters
                flash("The password must be at least seven characters", "error")
            elif not check_pw_conditions(password):
                # Flash alert - password must contain symbol, number, and capital
                flash("The password must contain a special symbol, a number, and a capital letter", "error")
            elif not valid_email(email):
                 # Flash alert - password must contain symbol, number, and capital
                flash("Please Enter a Valid Email", "error")
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                try:
                    new_user = User(email=email, username=username, password=hashed.decode('utf-8'))
                    db.session.add(new_user)
                    db.session.commit()
                except Exception:
                    flash("Sorry, there was an error. Try again later", "error")
                    return render_template("signup.html")
                # Flash alert - user created, redirect to home
                flash("Account Created", "success")
    return render_template("signup.html")
