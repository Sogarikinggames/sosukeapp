from . import db
from flask_login import UserMixin
from datetime import datetime
import pytz

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    img_name = db.Column(db.String(100), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=True)

