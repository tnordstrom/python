# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout_view, name="logout"),
    path("playlist/<str:playlist_id>/", views.playlist_detail, name="playlist_detail"),
    path("album/<str:album_id>/", views.album_detail, name="album_detail"),
    path("liked-songs/", views.liked_songs, name="liked_songs"),
    path("play/<str:track_uri>/", views.play_track, name="play_track"),
]
