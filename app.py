"""Blogly application."""

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
def show_all_users():
    """Retrieve user names and list"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.get('/users/new')
def show_new_user_form():
    return render_template("new_user_form.html")


@app.post('/users/new')
def process_form_and_add_user():
    """Pull data from form, make new user instance in DB, go back to user list"""
    response = request.form
    print(f"*********************************************{response}")

    return redirect('/users')



