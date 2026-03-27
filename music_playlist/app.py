import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, flash
from slugify import slugify

from models import db, Playlist, Track
from metadata import fetch_metadata, detect_source

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///playlists.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
db.init_app(app)


def _format_duration(seconds):
    """Convert total seconds to H:MM:SS or M:SS string."""
    if seconds is None:
        return ""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

app.jinja_env.filters["duration"] = _format_duration


with app.app_context():
    db.create_all()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _unique_slug(name: str) -> str:
    base = slugify(name) or "playlist"
    slug, n = base, 1
    while Playlist.query.filter_by(slug=slug).first():
        slug = f"{base}-{n}"
        n += 1
    return slug


# ---------------------------------------------------------------------------
# Routes: playlists
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    playlists = Playlist.query.order_by(Playlist.created_at.desc()).all()
    return render_template("index.html", playlists=playlists)


@app.route("/new", methods=["GET", "POST"])
def new_playlist():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Playlist name is required.", "error")
            return render_template("new_playlist.html")
        slug = _unique_slug(name)
        playlist = Playlist(slug=slug, name=name, description=description)
        db.session.add(playlist)
        db.session.commit()
        return redirect(url_for("view_playlist", slug=slug))
    return render_template("new_playlist.html")


@app.route("/p/<slug>")
def view_playlist(slug):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    return render_template("playlist.html", playlist=playlist)


@app.route("/p/<slug>/edit", methods=["GET", "POST"])
def edit_playlist(slug):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Playlist name is required.", "error")
        else:
            playlist.name = name
            playlist.description = description
            db.session.commit()
            flash("Playlist updated.", "success")
            return redirect(url_for("view_playlist", slug=slug))
    return render_template("edit_playlist.html", playlist=playlist)


@app.route("/p/<slug>/delete", methods=["POST"])
def delete_playlist(slug):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    db.session.delete(playlist)
    db.session.commit()
    flash("Playlist deleted.", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Routes: tracks
# ---------------------------------------------------------------------------

@app.route("/p/<slug>/add", methods=["POST"])
def add_track(slug):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    url = request.form.get("url", "").strip()
    note = request.form.get("note", "").strip()

    if not url:
        flash("Please enter a song URL.", "error")
        return redirect(url_for("view_playlist", slug=slug))

    if not detect_source(url):
        flash("URL must be from music.apple.com or bandcamp.com.", "error")
        return redirect(url_for("view_playlist", slug=slug))

    try:
        meta = fetch_metadata(url)
    except Exception as exc:
        flash(f"Could not fetch track info: {exc}", "error")
        return redirect(url_for("view_playlist", slug=slug))

    max_pos = db.session.query(db.func.max(Track.position)).filter_by(
        playlist_id=playlist.id
    ).scalar() or 0

    track = Track(
        playlist_id=playlist.id,
        url=url,
        source=meta["source"],
        title=meta["title"],
        artist=meta["artist"],
        album=meta["album"],
        artwork_url=meta["artwork_url"],
        embed_url=meta["embed_url"],
        duration_seconds=meta.get("duration_seconds"),
        position=max_pos + 1,
        note=note,
    )
    db.session.add(track)
    db.session.commit()
    return redirect(url_for("view_playlist", slug=slug))


@app.route("/p/<slug>/track/<int:track_id>/delete", methods=["POST"])
def delete_track(slug, track_id):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    track = Track.query.filter_by(id=track_id, playlist_id=playlist.id).first_or_404()
    db.session.delete(track)
    db.session.commit()
    return redirect(url_for("view_playlist", slug=slug))


@app.route("/p/<slug>/track/<int:track_id>/note", methods=["POST"])
def update_note(slug, track_id):
    playlist = Playlist.query.filter_by(slug=slug).first_or_404()
    track = Track.query.filter_by(id=track_id, playlist_id=playlist.id).first_or_404()
    track.note = request.form.get("note", "").strip()
    db.session.commit()
    return redirect(url_for("view_playlist", slug=slug))


# ---------------------------------------------------------------------------
# API: metadata preview (used by JS before submission)
# ---------------------------------------------------------------------------

@app.route("/api/preview")
def api_preview():
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    if not detect_source(url):
        return jsonify({"error": "Unsupported URL"}), 400
    try:
        meta = fetch_metadata(url)
        return jsonify(meta)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
