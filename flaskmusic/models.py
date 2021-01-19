
from datetime import datetime
from flask_login import UserMixin

from flaskmusic import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # This method going to print out whenever we create an artist
    def __repr__(self):
        return "<User {}: {} {}>".format(self.username, self.email, self.password)
        # return  f"User('{self.username}, '{self.email}', '{self.image_file}')"


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(25), unique=True, nullable=False)
    song = db.Column(db.String(50), nullable=False)
    album = db.Column(db.String(50), nullable=False)
    song_release_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())

    # This method going to print out whenever we create an artist
    def __repr__(self):
        return "<New Artist {}: {} - {}, {}, {}>".format(self.id, self.artist, self.song, self.album,
                                                         self.song_release_date)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=True, nullable=True, default='/static/img/default.png')
    album_release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # This method going to print out whenever we create an album
    def __repr__(self):
        return "<New Artist {}: {} - {}, {}, {}>".format(self.id, self.title, self.image_file, self.album_release_date)