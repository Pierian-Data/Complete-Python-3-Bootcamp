"""
Fetch track metadata from Apple Music and Bandcamp URLs.
"""

import json
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def detect_source(url: str) -> str | None:
    """Return 'apple', 'bandcamp', or None."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    if "music.apple.com" in host:
        return "apple"
    if "bandcamp.com" in host:
        return "bandcamp"
    return None


# ---------------------------------------------------------------------------
# Apple Music
# ---------------------------------------------------------------------------

def _apple_music_ids(url: str) -> tuple[str | None, str | None]:
    """Extract (album_id, track_id) from an Apple Music URL."""
    # https://music.apple.com/us/album/song-name/ALBUM_ID?i=TRACK_ID
    # https://music.apple.com/us/song/name/TRACK_ID
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    track_id = qs.get("i", [None])[0]

    path_parts = parsed.path.rstrip("/").split("/")
    numeric = [p for p in path_parts if p.isdigit()]

    if track_id:
        album_id = numeric[0] if numeric else None
        return album_id, track_id

    # /song/ path
    if "song" in path_parts and numeric:
        return None, numeric[-1]

    # album-only link – use last numeric segment as album_id
    if numeric:
        return numeric[-1], None

    return None, None


def fetch_apple_music(url: str) -> dict:
    album_id, track_id = _apple_music_ids(url)
    lookup_id = track_id or album_id
    if not lookup_id:
        raise ValueError(f"Could not extract track/album ID from URL: {url}")

    api_url = f"https://itunes.apple.com/lookup?id={lookup_id}"
    resp = requests.get(api_url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results", [])
    if not results:
        raise ValueError("iTunes API returned no results")

    # Prefer a track (wrapperType == 'track') over a collection
    track = next(
        (r for r in results if r.get("wrapperType") == "track"), results[0]
    )

    title = track.get("trackName") or track.get("collectionName", "Unknown")
    artist = track.get("artistName", "")
    album = track.get("collectionName", "")
    artwork = track.get("artworkUrl100", "").replace("100x100", "600x600")
    millis = track.get("trackTimeMillis")
    duration = int(millis / 1000) if millis else None

    # Build embed URL
    if track_id and album_id:
        embed = f"https://embed.music.apple.com/us/album/{album_id}?i={track_id}"
    elif track_id:
        embed = f"https://embed.music.apple.com/us/song/{track_id}"
    elif album_id:
        embed = f"https://embed.music.apple.com/us/album/{album_id}"
    else:
        embed = ""

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "artwork_url": artwork,
        "embed_url": embed,
        "duration_seconds": duration,
        "source": "apple",
    }


# ---------------------------------------------------------------------------
# Bandcamp
# ---------------------------------------------------------------------------

def _parse_iso_duration(s: str) -> int | None:
    """Parse ISO 8601 duration like PT3M45S into total seconds."""
    if not s:
        return None
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s)
    if not m:
        return None
    h, mins, secs = (int(x) if x else 0 for x in m.groups())
    total = h * 3600 + mins * 60 + secs
    return total if total > 0 else None


def _bandcamp_embed_url(url: str, track_id: str | None, album_id: str | None) -> str:
    if track_id:
        return f"https://bandcamp.com/EmbeddedPlayer/track={track_id}/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/artwork=small/"
    if album_id:
        return f"https://bandcamp.com/EmbeddedPlayer/album={album_id}/size=large/bgcol=ffffff/linkcol=0687f5/artwork=small/"
    return ""


def fetch_bandcamp(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # ---- Open Graph fallback values ----
    og_title = (soup.find("meta", property="og:title") or {}).get("content", "")
    og_image = (soup.find("meta", property="og:image") or {}).get("content", "")
    og_site = (soup.find("meta", property="og:site_name") or {}).get("content", "")

    # ---- Try JSON-LD (most reliable) ----
    title, artist, album = og_title, og_site, ""
    track_id = album_id = None
    duration = None

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string or "")
            if isinstance(ld, list):
                ld = ld[0]
            schema_type = ld.get("@type", "")
            if schema_type in ("MusicRecording", "MusicAlbum"):
                title = ld.get("name", title)
                by_artist = ld.get("byArtist", {})
                artist = by_artist.get("name", artist) if isinstance(by_artist, dict) else artist
                in_album = ld.get("inAlbum", {})
                album = in_album.get("name", "") if isinstance(in_album, dict) else ""
                duration = _parse_iso_duration(ld.get("duration", ""))
        except (json.JSONDecodeError, AttributeError):
            pass

    # ---- Extract numeric IDs from page data-tralbum or inline JS ----
    # Bandcamp embeds IDs in a data attribute on the player div
    player_div = soup.find("div", {"id": "trackInfo"}) or soup.find(
        "div", {"data-tralbum": True}
    )
    if player_div and player_div.get("data-tralbum"):
        try:
            tralbum = json.loads(player_div["data-tralbum"])
            track_id = str(tralbum.get("id", "")) or None
        except (json.JSONDecodeError, KeyError):
            pass

    # Fallback: scan inline <script> for TralbumData
    if not track_id and not album_id:
        scripts = soup.find_all("script")
        for s in scripts:
            text = s.string or ""
            # Look for track_id or item_id
            m = re.search(r'"track_id"\s*:\s*(\d+)', text)
            if m:
                track_id = m.group(1)
                break
            m = re.search(r'"id"\s*:\s*(\d+)', text)
            if m and "/track/" in url:
                track_id = m.group(1)
                break
            m = re.search(r'"id"\s*:\s*(\d+)', text)
            if m and "/album/" in url:
                album_id = m.group(1)
                break

    # Derive type from URL if still missing
    if not track_id and not album_id:
        if "/track/" in url:
            m = re.search(r'/track/[^/]+/?(\d+)?', url)
        else:
            m = None
        # Last resort: try og:url canonical scraping is done — leave IDs empty

    embed = _bandcamp_embed_url(url, track_id, album_id)

    return {
        "title": title or "Unknown",
        "artist": artist or "",
        "album": album or "",
        "artwork_url": og_image or "",
        "embed_url": embed,
        "duration_seconds": duration,
        "source": "bandcamp",
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def fetch_metadata(url: str) -> dict:
    """Fetch metadata for an Apple Music or Bandcamp URL."""
    source = detect_source(url)
    if source == "apple":
        return fetch_apple_music(url)
    if source == "bandcamp":
        return fetch_bandcamp(url)
    raise ValueError(f"Unsupported URL. Must be music.apple.com or *.bandcamp.com: {url}")
