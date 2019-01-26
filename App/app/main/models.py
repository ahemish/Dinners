from run import db
from flask_login import UserMixin


class User(db.Model ,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    full_name = db.Column(db.String(30))
    email_address = db.Column(db.String(200), unique=True)
    created_at = db.Column(db.DateTime())

class Favourite(db.Model ,UserMixin):
    __tablename__ = "favourite_dinners"
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    selected_at = db.Column(db.DateTime())

class Image(db.Model ,UserMixin):
    __tablename__ = "image_metadata"
    id = db.Column(db.Integer, primary_key=True)
    name_tag = db.Column(db.Integer)
    image_path = db.Column(db.Integer, unique=True)
    image_name = db.Column(db.String(200),unique=True)
    created_at = db.Column(db.DateTime())