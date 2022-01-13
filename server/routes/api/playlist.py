from flask import Flask

from db import DBHandler
from routes.auth.authentication import check_api_authentication


def add_playlist_routes(app: Flask, db: DBHandler):
    @app.route('/api/playlist/<string:playlist_id>/info/', methods=['GET'])
    @check_api_authentication(db)
    def route_playlist_info_get(playlist_id: str):
        return db.get_playlist_info(playlist_id)

    @app.route('/api/playlist/<string:playlist_id>/tracks/', methods=['GET'])
    @check_api_authentication(db)
    def route_playlist_tracks_get(playlist_id: str):
        return db.get_playlist_tracks(playlist_id)
