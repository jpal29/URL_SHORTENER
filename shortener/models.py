from flask import current_app, g
from flask.cli import with_appcontext
from app import db


class User(db.Model):
    """
    Create the User table
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Url(db.Model):
    """
    Create the URL table table
    """

    __tablename__='url'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    long_link = db.Column(db.String(250))
    short_link = db.Column(db.String(60))

    def __repr__(self):
        return '<Link: {}>'.format(self.id)

