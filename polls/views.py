# polls/views.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler
from spotipy.exceptions import SpotifyException
from django.shortcuts import render, redirect

def get_spotify_oauth(token_info=None):
    # MemoryCacheHandler prevents Spotipy from writing a local .cache file
    cache_handler = MemoryCacheHandler(token_info=token_info)
    
    return SpotifyOAuth(
        client_id="2ef5a00456ae427b92bdbc2d1db1f7c7",
        client_secret="9f927824194d42548a1d03cf9c199a88",
        redirect_uri="http://127.0.0.1:8000/callback/",
        scope="user-library-read playlist-read-private playlist-read-collaborative user-modify-playback-state user-read-playback-state",
        cache_handler=cache_handler,
        open_browser=False,
        show_dialog=True
    )

def get_valid_token(request):
    """Helper to retrieve and refresh the session token if needed."""
    token_info = request.session.get("spotify_token_info")
    if not token_info:
        return None
    sp_oauth = get_spotify_oauth(token_info=token_info)
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        request.session["spotify_token_info"] = token_info
    return token_info

def artist_sort_key(album):
    artist = album["artists"].lower().strip()
    for prefix in ("the ", "a ", "an "):
        if artist.startswith(prefix):
            artist = artist[len(prefix):]
            break  # Only strip one leading article
    return (artist, album["name"].lower())

def index(request):
    token_info = get_valid_token(request)

    if not token_info:
        sp_oauth = get_spotify_oauth()
        context = {
            "heading": "Spotify Library Explorer",
            "is_logged_in": False,
            "auth_url": sp_oauth.get_authorize_url(),
        }
        return render(request, "polls/index.html", context)

    sp = spotipy.Spotify(auth=token_info["access_token"])

    # 1. Fetch Playlists safely
    playlists = sp.current_user_playlists(limit=50) or {}
    playlist_data = [
        {"id": p["id"], "name": p["name"]}
        for p in (playlists.get("items") or [])
        if p and p.get("id") and p.get("name")
    ]

    # 2. Fetch ALL Saved Albums safely via pagination
    album_data = []
    results = sp.current_user_saved_albums(limit=50)
    while results:
        for item in (results.get("items") or []):
            if not item:
                continue
            album = item.get("album")
            if album and album.get("id") and album.get("name"):
                artists = ", ".join(
                    a["name"] for a in (album.get("artists") or []) if a and a.get("name")
                )
                album_data.append({
                    "id": album["id"],
                    "name": album["name"],
                    "artists": artists,
                })
        results = sp.next(results) if results.get("next") else None

    album_data.sort(key=artist_sort_key)
        
    context = {
        "heading": "My Spotify Library",
        "is_logged_in": True,
        "playlists": playlist_data,
        "albums": album_data,
    }
    return render(request, "polls/index.html", context)
    
def playlist_detail(request, playlist_id):
    token_info = get_valid_token(request)
    if not token_info:
        return redirect("index")

    sp = spotipy.Spotify(auth=token_info["access_token"])

    # Fetch playlist metadata (just the name) and items separately
    playlist_meta = sp.playlist(playlist_id, fields="name")
    results = sp.playlist_items(playlist_id)

    tracks = []
    for item in results.get("items", []):
        # Spotify uses "track" (or "item" in newer API versions)
        track = item.get("track") or item.get("item")
        if track and track.get("name") and track.get("id"):
            artists = ", ".join(
                artist["name"] for artist in track.get("artists", [])
            )
            tracks.append({
                "id": track["id"],
                "uri": track["uri"],
                "name": track["name"],
                "artists": artists,
            })

    context = {
        "playlist_name": playlist_meta.get("name", "Playlist"),
        "tracks": tracks,
    }
    return render(request, "polls/playlist_detail.html", context)

def callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get("code")
    if code:
        # Exchange the authorization code for token_info and save it in the session
        token_info = sp_oauth.get_access_token(code)
        request.session["spotify_token_info"] = token_info
    return redirect("index")
    
def logout_view(request):
    # Remove the Spotify token from the Django session
    request.session.pop("spotify_token_info", None)
    return redirect("index")
    
def liked_songs(request):
    token_info = get_valid_token(request)
    if not token_info:
        return redirect("index")

    sp = spotipy.Spotify(auth=token_info["access_token"])
    results = sp.current_user_saved_tracks(limit=50)

    tracks = []
    for item in results.get("items", []):
        track = item.get("track")
        if track and track.get("name") and track.get("id"):
            artists = ", ".join(a["name"] for a in track.get("artists", []))
            tracks.append({
                "id": track["id"],
                "uri": track.get("uri"),
                "name": track["name"],
                "artists": artists,
            })

    context = {
        "playlist_name": "Liked Songs",
        "tracks": tracks,
        "error_message": None,
    }
    return render(request, "polls/playlist_detail.html", context)


def album_detail(request, album_id):
    token_info = get_valid_token(request)
    if not token_info:
        return redirect("index")

    sp = spotipy.Spotify(auth=token_info["access_token"])
    album = sp.album(album_id)
    results = sp.album_tracks(album_id, limit=50)

    tracks = []
    for track in results.get("items", []):
        if track and track.get("name") and track.get("id"):
            artists = ", ".join(a["name"] for a in track.get("artists", []))
            tracks.append({
                "id": track["id"],
                "uri": track.get("uri"),
                "name": track["name"],
                "artists": artists,
            })

    context = {
        "playlist_name": f"{album.get('name', 'Album')}",
        "tracks": tracks,
        "error_message": None,
    }
    return render(request, "polls/playlist_detail.html", context)
        
def play_track(request, track_uri):
    token_info = get_valid_token(request)
    if not token_info:
        return redirect("index")

    sp = spotipy.Spotify(auth=token_info["access_token"])
    try:
        # Plays on whichever device currently has Spotify open/active
        sp.start_playback(uris=[track_uri])
    except SpotifyException as e:
        print("Playback error (make sure Spotify is open on a device):", e)

    # Return to the previous playlist page
    return redirect(request.META.get("HTTP_REFERER", "index"))
