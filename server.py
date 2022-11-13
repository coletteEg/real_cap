import email
from wsgiref.util import request_uri
from flask import (Flask, render_template, request, flash, session, redirect, url_for)
import os

from sqlalchemy import null
from model import connect_to_db, db, Shark, User
import crud
from jinja2 import StrictUndefined
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'sharks_are_the_best'
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def home():
    return render_template ("homepage.html")

@app.route("/sharks")
def all_sharks():
    all_sharks = crud.get_all_sharks()
    return render_template ("sharks.html", all_sharks = all_sharks)

@app.route("/users")
def users():
    all_users = crud.get_users()
    return render_template("users.html", all_users=all_users)

@app.route("/users", methods=["POST"])
def register():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    tobechecked = crud.get_user_by_email(user_email)
    if tobechecked == None:
        new_user = crud.create_user(user_email, user_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("User Created")
    else:
        flash("This email is already being used")
    return redirect("/")

@app.route("/login", methods=["POST", 'GET'])
def login():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    user_q = User.query.filter_by(email = user_email).first()
    if user_q.email == user_email and user_q.password == user_pass:
        session['user_id'] = user_q.user_id
        flash("You are now logged in")
        
    else:
        flash("User not found. Please Register.")
    return redirect("/")

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm()
#     email = login_form.email.data
#     password = login_form.password.data
#     if login_form.validate_on_submit():
#         user = crud.find_user(email)
#         if user:
#             if user.password == password:
#                 login_user(user)
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("No user found. Check your credentials and try again!")
#                 return redirect(url_for('home'))
#         else:
#                 flash("No user found. Check your credentials and try again!")
#                 return redirect(url_for('home'))
#     else:
#         return redirect(url_for("home"))

@app.route('/logout')
def logout():
    if 'user_in' in session:
        del session['user_id']
        flash('You have logged out')
    else:
        flash("Uh oh youre not logged in!")
    return redirect('/')

@app.route("/users/<user_id>")
def user_details(user_id):
    detailed_user = User.query.get(user_id)
    return render_template ("user_details.html", detailed_user=detailed_user)

@app.errorhandler(404)
def notfound(e):
   return render_template('404.html')

if __name__== '__main__':
    app.env = 'development'
    connect_to_db(app)
    app.run(debug=True, port = 5432, host= 'localhost')