"""Blogly application."""

from http.client import ResponseNotReady
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_users():
    return redirect('/users')


@app.get('/users')
def display_all_users():
    """Retrieve user names and display list"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.get('/users/new')
def display_new_user_form():
    return render_template("new_user_form.html")


@app.post('/users/new')
def process_form_and_add_user():
    """Pull data from form, make new user instance in DB, go back to user list"""
    response = request.form
    print(f"*********************************************{response}")
    first_name = response["first-name"]
    last_name = response["last-name"]
    image_url = response["image-url"]

    user = User(first_name = first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get("/users/<int:user_id>")
def display_user_info(user_id):
    """Retrieve user data via id and display user info"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.get("/users/<int:user_id>/edit")
def display_edit_user_form(user_id):
    """"""
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.post("/users/<int:user_id>/edit")
def process_edit_info(user_id):
    """"""
    response = request.form
    print(f"*********************************************{response}")
    first_name = response["first-name"]
    last_name = response["last-name"]
    image_url = response["image-url"]

    user = User.query.get_or_404(user_id)
    user.first_name =first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')