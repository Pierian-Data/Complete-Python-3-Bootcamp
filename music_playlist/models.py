from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tracks = db.relationship(
        "Track", backref="playlist", lazy=True, order_by="Track.position"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "description": self.description,
            "track_count": len(self.tracks),
        }


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(20), nullable=False)  # "apple" or "bandcamp"
    title = db.Column(db.String(300), nullable=False)
    artist = db.Column(db.String(300), default="")
    album = db.Column(db.String(300), default="")
    artwork_url = db.Column(db.String(500), default="")
    embed_url = db.Column(db.String(500), default="")
    duration_seconds = db.Column(db.Integer, nullable=True)
    position = db.Column(db.Integer, default=0)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "source": self.source,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "artwork_url": self.artwork_url,
            "embed_url": self.embed_url,
            "position": self.position,
            "note": self.note,
        }
