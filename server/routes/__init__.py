from flask import Flask

from db import DBHandler

from routes.main.main import add_main_routes
from routes.auth.authentication import add_authentication_routes
from routes.api.artist import add_artist_routes
from routes.api.album import add_album_routes
from routes.api.playlist import add_playlist_routes
from routes.api.track import add_track_routes
from routes.api.search import add_search_routes
from routes.player.player import add_player_routes


def add_routes(app: Flask, db: DBHandler):
    for add_func in [add_main_routes, add_authentication_routes,
                     add_artist_routes, add_album_routes, add_playlist_routes,
                     add_track_routes, add_search_routes, add_player_routes]:
        add_func(app, db)
