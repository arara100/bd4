# models.py
from app import db

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('Song.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    downloads = db.relationship('Download', back_populates='user')
    favorite_songs = db.relationship('Song', secondary=favorites, back_populates='fans')

class Song(db.Model):
    __tablename__ = 'Song'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(5, 2))
    release_date = db.Column(db.Date)

    downloads = db.relationship('Download', back_populates='song')
    fans = db.relationship('User', secondary=favorites, back_populates='favorite_songs')

class Download(db.Model):
    __tablename__ = 'Download'
    id = db.Column(db.Integer, primary_key=True)
    download_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id'))

    user = db.relationship('User', back_populates='downloads')
    song = db.relationship('Song', back_populates='downloads')

