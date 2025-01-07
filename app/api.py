from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import pandas as pd
from datetime import datetime

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

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.BigInteger, nullable=False)
    year = db.Column(db.Integer, nullable=False)

def bulk_insert_songs():
    songs = pd.read_csv('../model/data.csv')
    
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
    
# CHECK API HEALTH
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)