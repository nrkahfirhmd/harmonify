from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import pandas as pd
import numpy as np
from datetime import datetime
import random

app = Flask(__name__)

def setup_db():
    hostname = 'localhost'
    user = 'root'
    password = ''

    db = pymysql.connections.Connection(
        host=hostname,
        user=user,
        password=password
    )
    
    cursor = db.cursor()
    
    with app.app_context():
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS db_harmonify')
        cursor.close()
    
    cursor.close()
    db.close()

setup_db()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_harmonify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

session = {}

songs = pd.read_csv('../model/data.csv')
similarity = pd.read_csv('../model/results.csv')
similarity.drop('spotify_id', axis=1, inplace=True)
similarity = np.array(similarity)

song_query = ""
recommendations = {}

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    song = db.Column(db.String(255), nullable=False)
    playlist_id = db.Column(db.String(255), db.ForeignKey('playlists.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    songs_id = db.Column(db.Text, nullable=False)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.BigInteger, nullable=False)
    year = db.Column(db.Integer, nullable=False)

def bulk_insert_songs():
    with app.app_context():
        for index, row in songs.iterrows():
            song = Song(
                id=row['spotify_id'],
                name=row['name'],
                album=row['album_name'],
                artist=row['artists'],
                duration=row['duration_ms'],
                year=datetime.strptime(row['album_release_date'], "%Y-%m-%d").year
            )
            
            db.session.add(song)
        
        db.session.commit()

@app.route('/migrate-and-seed', methods=['POST'])
def migrate_and_seed():
    with app.app_context():
        db.create_all()
        
        user1 = User(username='ica071005', password='ica071005')
        user2 = User(username='kahfi061204', password='kahfi061204')
        
        bulk_insert_songs()

        db.session.add_all([user1, user2])
        db.session.commit()
        
        return jsonify({"message": "migrate and seed success!"}), 200
    
@app.route('/drop', methods=['POST'])
def drop():
    with app.app_context():
        db.drop_all()
        
        return jsonify({"message": "drop success!"}), 200
    
@app.route('/recommend/<id>/<int:top_n>', methods=['GET'])
def recommend(id, top_n):
    global recommendations, song_query
    song_query = id
    song_idx = songs.index[songs['spotify_id'] == id][0]
    similar_indices = similarity[song_idx].argsort()[::-1][1:top_n+1]
    recommendations = songs.iloc[similar_indices]
    
    return jsonify({"recommendations": recommendations.to_dict(orient='records')}), 200

@app.route('/login', methods=['POST'])
def login():
    global session
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['username'] = username
        session['logged_in'] = True
        return jsonify({"message": "login success!"}), 200
    else:
        return jsonify({"message": "login failed!"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    
    if password == confirm:
        user = User.query.filter_by(username=username).first()
        
        if user:
            return jsonify({"message": "username already exists!"}), 401
        else:
            new_user = User(username=username, password=password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({"message": "register success!"}), 200
    else:
        return jsonify({"message": "password and confirm password must be the same!"}), 401

@app.route('/save-result', methods=['GET'])
def save_result():
    global session, recommendations, song_query
    if not recommendations.empty and session.get('logged_in'):
        song_ids = ','.join(recommendations['spotify_id'].astype(str).values)
        
        random_id = create_random_id()
        
        playlist = Playlist(
            id=random_id,
            songs_id=song_ids
        )
        
        results = Result(
            id=create_random_id(),
            user_id=session['username'],
            playlist_id=random_id,
            song=song_query
        )
        
        db.session.add(playlist)
        db.session.add(results)
        db.session.commit()
        
        return jsonify({"message": "result saved!"}), 200
    else:
        return jsonify({"message": "result not saved!"}), 401
    
@app.route('/get-history', methods=['GET'])
def get_history():
    global session
    if session.get('logged_in'):
        query = Result.query.filter_by(user_id=session['username']).all()
        
        results = []
        for result in query:
            song = Song.query.filter_by(id=result.song).first()
            
            results.append({
                "track": song.name,
                "artist": song.artist,
                "created_at": result.created_at,
                "playlist_id": result.playlist_id 
            })
        
        return jsonify({"history": results}), 200
    else:
        return jsonify({"message": "you must login first!"}), 401
    
@app.route('/get-playlist/<id>', methods=['GET'])
def get_playlist(id):
    playlist = Playlist.query.filter_by(id=id).first()
    
    if playlist:
        song_ids = playlist.songs_id.split(',')
        songs = Song.query.filter(Song.id.in_(song_ids)).all()
        
        songs_list = [
            {
                "id": song.id,
                "name": song.name,
                "album": song.album,
                "artist": song.artist,
                "duration": song.duration,
                "year": song.year
            }
            for song in songs
        ]
        
        return jsonify({"playlist": songs_list}), 200
    else:
        return jsonify({"message": "playlist not found!"}), 404
    
def create_random_id():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    return ''.join(random.choice(characters) for i in range(10))
    
# CHECK API HEALTH
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)