from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
import datetime
app = Flask(__name__)
app.config.from_object(DevConfig)
db=SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts=db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )
tags=db.Table('post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
    )
class Post(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255))
    text=db.Column(db.Text())
    publish_date=db.Column(db.DateTime())
    comments=db.relationship(
        'Comment',
        backref='Post',
        lazy='dynamic'
    )
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
    tags=db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts',lazy='dynamic')
    )
class Tag(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255))
class Comment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'))
    text=db.Column(db.String(255))

#
def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

#
@app.route('/')
def home():
    return '<h1>Hello World!</h1>'
if __name__ == '__main__':
    app.run()