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

recommendations = []

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    playlist_id = db.Column(db.String(255), db.ForeignKey('playlists.id'), nullable=False)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    songs_id = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

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
    
@app.route('/recommend/<id>/<int:top_n>', methods=['GET'])
def recommend(id, top_n):
    song_idx = songs.index[songs['spotify_id'] == id][0]
    similar_indices = similarity[song_idx].argsort()[::-1][1:top_n+1]
    recommendations = songs.iloc[similar_indices]
    
    return jsonify({"recommendations": recommendations.to_dict(orient='records')}), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['username'] = username
        session['logged_in'] = True
        return jsonify({"message": "login success!"}), 200
    else:
        return jsonify({"message": "login failed!"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    confirm = request.json['confirm']
    
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
    
# CHECK API HEALTH
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)