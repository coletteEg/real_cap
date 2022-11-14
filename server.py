import email
from wsgiref.util import request_uri
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import login_user, login_required, logout_user, LoginManager
import os

from sqlalchemy import null
from model import Shark, User, db, connect_to_db
import crud
from jinja2 import StrictUndefined
from forms import LoginForm, UserForm, AddShark

app = Flask(__name__)
app.secret_key = 'sharks_are_the_best'
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return crud.User.query.filter_by(user_id = user_id).first()

@app.route("/")
def home():
    return render_template ("homepage.html")

@app.route("/sharks")
@login_required
def all_sharks():
    all_sharks = crud.get_all_sharks()
    return render_template ("sharks.html", all_sharks = all_sharks)

@app.route("/users")
def users():
    all_users = crud.get_users()
    return render_template("users.html", all_users=all_users)

@app.route('/confirmed')
@login_required
def confirmed_user():
    return render_template('confirmed.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('You have logged in!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('confirmed_user')

            return redirect(next)

    return render_template('login.html',form=form)

# @app.route('/logout')
# def logout():
#     if 'user_in' in session:
#         del session['user_id']
#         flash('You have logged out')
#     else:
#         flash("Uh oh youre not logged in!")
#     return redirect('/')

@app.route('/register',methods=['GET','POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    )
        db.session.add(user)
        db.session.commit()
        flash("Thanks for joining us!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route("/cart")
def show_cart():

   order_total = 0
   cart_shark = []

   cart = session.get("cart", {})

   for shark_id, quantity in cart.items():
      shark = shark.get_by_id(shark_id)

      total_cost = quantity * shark.price
      order_total += total_cost

      shark.quantity = quantity
      shark.total_cost = total_cost

      cart_shark.append(shark)

   return render_template("cart.html", cart_shark=cart_shark, order_total=order_total)

@app.route("/add_to_cart/<shark_id>")
def add_to_cart(shark_id):

   if 'cart' not in session:
      session['cart'] = {}
   cart = session['cart'] 

   cart[shark_id] = cart.get(shark_id, 0) + 1
   session.modified = True
   flash(f"Melon {shark_id} successfully added to cart.")
   print(cart)

   return redirect("/cart")

@app.route("/empty")
def empty_cart():
   session["cart"] = {}

   return redirect("/cart")

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
    app.run(debug=True, port = 9000, host= 'localhost')