"""Blogly application."""

from http.client import ResponseNotReady
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()
# **************************ALL USER ROUTES****************************************************************


# ***************DISPLAY USERS*********************
@app.get("/")
def redirect_to_users():
    return redirect("/users")


@app.get("/users")
def display_all_users():
    """Retrieve user names and display list"""

    users = User.query.all()
    return render_template("users.html", users=users)

# ***************NEW USER**************************
@app.get("/users/new")
def display_new_user_form():
    """Display new user form"""
    return render_template("new_user_form.html")


@app.post("/users/new")
def process_form_and_add_user():
    """Pull data from form, make new user instance in DB, go back to user list"""

    # REVIEW: reconsider response name, rename to "data"?
    response = request.form
    # TODO: check for empty string, check and use flash message
    first_name = response["first-name"]
    last_name = response["last-name"]
    image_url = response["image-url"]

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

# ***************DISPLAY USER*********************
@app.get("/users/<int:user_id>")
def display_user_info(user_id):
    """Retrieve user data via id and display user info"""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

# ***************EDIT USER************************
@app.get("/users/<int:user_id>/edit")
def display_edit_user_form(user_id):
    """Display edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit_info(user_id):
    """Retrieve user edit form data and update db"""

    user = User.query.get_or_404(user_id)
    # REVIEW: reconsider response name, rename to "data"?
    response = request.form
    # TODO: check for empty string, check and use flash message
    first_name = response["first-name"]
    last_name = response["last-name"]
    image_url = response["image-url"]

    
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

# ***************DELETE USER*********************
@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user from db"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# **************************************ALL POSTS ROUTES****************************************************************
@app.get("/users/<int:user_id>/posts/new")
def display_new_post_from(user_id):
    """Display new post form for user"""

    user = User.query.get_or_404(user_id)
    return render_template("new_post_form.html", user=user)

@app.post("/users/<int:user_id>/posts/new")
def process_new_post_form(user_id):
    """Retrieve new post form data, add to db"""

    data = request.form
    # TODO: check for empty string, check and use flash message
    title = data["title"]
    content = data["content"]
    
    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def display_post(post_id):
    """Display single post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post_detail.html", post=post, user=user)