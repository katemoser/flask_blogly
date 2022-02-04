from flask_sqlalchemy import SQLAlchemy, func


DEFAULT_IMAGE_URL = "https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg"
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    first_name = db.Column(db.String(50),
                        nullable=False)
    last_name = db.Column(db.String(50),
                        nullable=False)
    image_url = db.Column(db.Text,
                        nullable=True)

class Post(db.Model):
    """Post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, 
                        timezone = True, 
                        default = func.current_timestamp())
    user_id = db.Column(db.ForeignKey("users.id"))

    user = db.relationship('User',
                        backref='posts')