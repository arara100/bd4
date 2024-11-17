# routes.py
from app import app, db
from models import User, Song, Download
from flask import request, jsonify
from datetime import datetime

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    new_song = Song(title=data['title'], price=data['price'], release_date=data['release_date'])
    db.session.add(new_song)
    db.session.commit()
    return jsonify({"message": "Song created successfully"}), 201

@app.route('/download', methods=['POST'])
def add_download():
    data = request.get_json()
    user_id = data['user_id']
    song_id = data['song_id']
    download_date = datetime.now()

    new_download = Download(user_id=user_id, song_id=song_id, download_date=download_date)
    db.session.add(new_download)
    db.session.commit()
    return jsonify({"message": "Download added successfully"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify([{"id": song.id, "title": song.title, "price": str(song.price), "release_date": song.release_date} for song in songs])

@app.route('/downloads', methods=['GET'])
def get_downloads():
    downloads = Download.query.all()
    return jsonify([
        {"id": download.id, "user_id": download.user_id, "song_id": download.song_id, "download_date": download.download_date}
        for download in downloads
    ])


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()
    song = Song.query.get(song_id)

    if song:
        song.title = data.get('title', song.title)
        song.price = data.get('price', song.price)
        song.release_date = data.get('release_date', song.release_date)

        db.session.commit()
        return jsonify({"message": "Song updated successfully"}), 200
    else:
        return jsonify({"message": "Song not found"}), 404


@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = Song.query.get(song_id)

    if song:
        db.session.delete(song)
        db.session.commit()
        return jsonify({"message": "Song deleted successfully"}), 200
    else:
        return jsonify({"message": "Song not found"}), 404


@app.route('/downloads/<int:download_id>', methods=['PUT'])
def update_download(download_id):
    data = request.get_json()
    download = Download.query.get(download_id)

    if download:
        download.user_id = data.get('user_id', download.user_id)
        download.song_id = data.get('song_id', download.song_id)
        download.download_date = data.get('download_date', download.download_date)

        db.session.commit()
        return jsonify({"message": "Download updated successfully"}), 200
    else:
        return jsonify({"message": "Download not found"}), 404


@app.route('/downloads/<int:download_id>', methods=['DELETE'])
def delete_download(download_id):
    download = Download.query.get(download_id)

    if download:
        db.session.delete(download)
        db.session.commit()
        return jsonify({"message": "Download deleted successfully"}), 200
    else:
        return jsonify({"message": "Download not found"}), 404

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite_song(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    song = Song.query.get_or_404(data['song_id'])
    user.favorite_songs.append(song)
    db.session.commit()
    return jsonify({'message': 'Song added to favorites'})

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorite_songs(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([{'id': s.id, 'title': s.title} for s in user.favorite_songs])

@app.route('/users/<int:user_id>/favorites/<int:song_id>', methods=['DELETE'])
def remove_favorite_song(user_id, song_id):
    user = User.query.get_or_404(user_id)
    song = Song.query.get_or_404(song_id)
    user.favorite_songs.remove(song)
    db.session.commit()
    return jsonify({'message': 'Song removed from favorites'})


@app.route('/users/<int:user_id>/favorites/multiple', methods=['POST'])
def add_multiple_favorites_to_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    song_ids = data.get('song_ids', [])
    if not song_ids:
        return jsonify({'message': 'No song IDs provided'}), 400

    # Отримуємо пісні за їхніми ID
    songs = Song.query.filter(Song.id.in_(song_ids)).all()

    # Додаємо пісні до улюблених
    user.favorite_songs.extend([song for song in songs if song not in user.favorite_songs])
    db.session.commit()

    return jsonify({
        'message': 'Songs added to favorites',
        'user': {'id': user.id, 'username': user.username},
        'songs': [{'id': song.id, 'title': song.title} for song in user.favorite_songs]
    }), 200


@app.route('/songs/<int:song_id>/fans/multiple', methods=['POST'])
def add_multiple_users_to_song(song_id):
    data = request.get_json()
    song = Song.query.get_or_404(song_id)

    user_ids = data.get('user_ids', [])
    if not user_ids:
        return jsonify({'message': 'No user IDs provided'}), 400

    # Отримуємо користувачів за їхніми ID
    users = User.query.filter(User.id.in_(user_ids)).all()

    # Додаємо користувачів до фанів пісні
    song.fans.extend([user for user in users if user not in song.fans])
    db.session.commit()

    return jsonify({
        'message': 'Users added as fans',
        'song': {'id': song.id, 'title': song.title},
        'users': [{'id': user.id, 'username': user.username} for user in song.fans]
    }), 200



